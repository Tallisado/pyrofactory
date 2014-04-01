import json
import os
import platform
#'[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

class BrowserMode(Enum):
    SauceMultiple = 1
    SauceSingle = 2
    SauceSolo = 3
    LocalSolo = 4
    
class BrowserData:
    def __init__(self, config):
        self.url_list = []
        
        # command line overrides
        use_cmdline_username = use_cmdline_accesskey = use_cmdline_display = use_cmdline_local_solo = use_cmdline_browser_sauce = use_cmdline_base_url = False
        if os.environ.get('BASE_URL'):
            print '(BrowserData) BASE_URL found in commandline - will supercede config value'
            use_cmdline_base_url = True        
        if os.environ.get('SAUCE_USERNAME'):
            print '(BrowserData) SAUCE_USERNAME found in commandline - will supercede sauce url'
            use_cmdline_username = True
        if os.environ.get('SAUCE_ACCESSKEY'):
            print '(BrowserData) SAUCE_ACCESSKEY found in commandline - will supercede sauce url'
            use_cmdline_accesskey = True           
        if os.environ.get('DISPLAY'):
            print '(BrowserData) SAUCE_ACCESSKEY found in commandline - will supercede sauce url and/or config'
            use_cmdline_display = True
        if os.environ.get('BROWSER'):
            if len(browser_mode.split(',')) == 3:
                print '(BrowserData) BROWSER found in commandline - will supercede config for sauce solo'
                use_cmdline_browser_sauce = True
            elif os.environ.get('BROWSER') in ["firefox", "chrome"]
                print '(BrowserData) BROWSER found in commandline - will supercede config for local solo'
                use_cmdline_local_solo = True
            else:
                raise NameError('(BrowserData) ERROR BROWSER found in commandline did not match requirements for sauce or local solo') 
                # show usage
                # os=Linux&browser=chrome&browser-version=32

        
        # determine browser mode
        if os.environ.get('SAUCE_ONDEMAND_BROWSERS') :
            print '(BrowserData) SAUCE_ONDEMAND_BROWSERS was intersected - Sauce Multiple mode enabled.'
            browser_mode = BrowserMode.SauceMultiple
        elif os.environ.get('SELENIUM_DRIVER'):
            print '(BrowserData) SELENIUM_DRIVER was intersected - Sauce Multiple mode enabled.'
            browser_mode = BrowserMode.SauceSingle
        else:
            if use_cmdline_sauce_solo:
                print '(BrowserData) no environment settings were intersected - Sauce Solo enabled'
                browser_mode = BrowserMode.SauceSolo
            else #use_cmdline_local_solo
                print '(BrowserData) no environment settings were intersected - Local Solo enabled'
                browser_mode = BrowserMode.LocalSolo
        
        # parse and store urls
        if browser_mode == BrowserMode.SauceMultiple:
            self.raw_json = json.loads(os.environ.get('SAUCE_ONDEMAND_BROWSERS')) 
            for browser_item in self.raw_json:            
                if 'url' in browser_item:
                    self.url_list.append(browser_item['url'])                    
        elif browser_mode == BrowserMode.SauceSingle:
            self.url_list.append(os.environ.get('SELENIUM_DRIVER'))            
        elif browser_mode == BrowserMode.LocalSolo:
            default_url = config.DEFAULT_SAUCEURL % (os.getenv('SAUCE_USERNAME', config.SAUCE_USERNAME), os.getenv('SAUCE_ACCESSKEY', config.SAUCE_ACCESSKEY), config.DEFAULT_SOLO_BROWSER)
            self.url_list.append(default_url)
        
        # use overrides in place of the urls            
        for browser_item in self.url_list:
            browser_item['username'] = os.environ.get('SAUCE_USERNAME') if use_cmdline_username
            browser_item['access-key'] = os.environ.get('SAUCE_ACCESSKEY') if use_cmdline_accesskey
            browser_item['browser'] = os.environ.get('BROWSER') if use_cmdline_local_solo
            if use_cmdline_browser_sauce:
                # os=Linux&browser=chrome&browser-version=32
                browser_item['os'],browser_item['browser'],browser_item['browser-version'] = browser_mode.split(',')
                
    def setRuntimeENV(self, i, config, test_name):
        os.environ['BASE_URL'] = config.BASE_URL if not use_cmdline_base_url   
        os.environ["PYBROWSER"] = self.getBrowser(i) if use_cmdline_local_solo:
        os.environ["PYROBOT_REMOTE_URL"] = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (self.getUserName(i), self.getAccessKey(i))
        os.environ["PYROBOT_CAPS"] = 'name:%s,platform:%s,version:%s,browserName:%s,javascriptEnabled:True' % (test_name, self.getOS(i), self.getBrowserVersion(i), self.getBrowser(i))
        os.environ['DISPLAY'] = config.DEFAULT_BROWSER_DISPLAY if not use_cmdline_display
        
        print '(BrowserData)[setPyrobotEnvForTest] BASE_URL:            %s' %  os.environ['BASE_URL']
        print '(BrowserData)[setPyrobotEnvForTest] PYROBOT_REMOTE_URL:  %s' %  os.environ['PYROBOT_REMOTE_URL']
        print '(BrowserData)[setPyrobotEnvForTest] PYROBOT_CAPS:        %s' %  os.environ['PYROBOT_CAPS']
        print '(BrowserData)[setPyrobotEnvForTest] DISPLAY     :        %s' %  os.environ['DISPLAY']
            
    def getUrlCount(self):
        return len(self.url_list)
        
    def getUrlString(self, index):
        return self.url_list[index]
    
    def getUrlHash(self, index):
        self.fields = {}
        fields = self.url_list[index].split(':')[1][1:].split('&')
        for field in fields:
            [key, value] = field.split('=')   
            self.fields[key] = value
        return self.fields
        
    def getValue(self, target_key, index):   
        fields = self.getUrlHash(index)
        if target_key in fields:
            return fields[target_key]
        else:
            return None

    def getBrowser(self, index):
        if browser_mode == BrowserMode.LocalSolo:
            return 'localbrowser'
        else:
            return self.getValue("browser", index)
            
    def getOS(self, index):
        if browser_mode == BrowserMode.LocalSolo:
            return platform.system() 
        else:
            return self.getValue("os", index)

    def getBrowserVersion(self, index):        
        if browser_mode == BrowserMode.LocalSolo:
            return 'localver'
        else:
            return self.getValue('browser-version', index)
            
    def getUserName(self, index):
        return self.getValue("username", index)

    def getAccessKey(self, index):
        return self.getValue("access-key", index)

    def getJobName(self, index):
        return self.getValue("job-name", index)


    def getFirefoxProfileURL(self, index):
        return self.getValue('firefox-profile-url', index)

    def getMaxDuration(self, index):
        try:
            return int(self.getValue('max-duration', index))
        except:
            return 0

    def getIdleTimeout(self, index):
        try:
            return int(self.getValue('idle-timeout', index))
        except:
            return 0

    def getUserExtensionsURL(self, index):
        return self.getValue('user-extensions-url', index)    
            