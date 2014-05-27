import json
import os
import platform
#from enum import Enum
#'[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

def enum(**enums):
    return type('Enum', (), enums)
    
# class BrowserMode(Enum):
    # SauceMultiple = 1
    # SauceSingle = 2
    # SauceSolo = 3
    # LocalSolo = 4
    
BrowserMode = enum(SauceMultiple=1, SauceSingle=2, SauceSolo=3, LocalSolo=4)
    
class BrowserData:
    def __init__(self, config):
        self.url_list = []
        
        # command line overrides
        usecmdline_username = usecmdline_accesskey = self.usecmdline_display = self.usecmdline_browser_localformat = usecmdline_browser_sauceformat = self.usecmdline_base_url = False
        if os.environ.get('BASE_URL'):
            print '(BrowserData)[init] CMDLINE Found: BASE_URL; superceded config value'
            self.usecmdline_base_url = True        
        if os.environ.get('SAUCE_USERNAME'):
            print '(BrowserData)[init] CMDLINE Found: SAUCE_USERNAME; superceded sauce url'
            usecmdline_username = True
        if os.environ.get('SAUCE_ACCESSKEY'):
            print '(BrowserData)[init] CMDLINE Found: SAUCE_ACCESSKEY; superceded sauce url'
            usecmdline_accesskey = True           
        if os.environ.get('DISPLAY'):
            print '(BrowserData)[init] CMDLINE Found: DISPLAY; superceded config value'
            self.usecmdline_display = True
        if os.environ.get('BROWSER'):
            if len(os.environ.get('BROWSER').split(',')) == 3:
                print '(BrowserData)[init] CMDLINE Found: BROWSER; superceded config (Trigger: Sauce Solo)'
                usecmdline_browser_sauceformat = True
            elif os.environ.get('BROWSER') in ["firefox", "chrome"]:
                print '(BrowserData)[init] CMDLINE Found: BROWSER; superceded config (Trigger: Local Solo)'
                self.usecmdline_browser_localformat = True
            else:   
                # raise error and catch when this class is instantiated
                print '(BrowserData)[init] CMDLINE Found: BROWSER; ERROR'
                raise NameError('(BrowserData) ERROR BROWSER found in commandline did not match requirements for sauce or local solo') 
                # show usage
                # os=Linux&browser=chrome&browser-version=32

        
        # determine browser mode
        if os.environ.get('SAUCE_ONDEMAND_BROWSERS') :
            print '(BrowserData)[init] ENV Intersected: SAUCE_ONDEMAND_BROWSERS (Sauce Multiple) mode enabled'
            self.browser_mode = BrowserMode.SauceMultiple
        elif os.environ.get('SELENIUM_DRIVER'):
            print '(BrowserData)[init] ENV Intersected: SELENIUM_DRIVER (Sauce Single) mode enabled'
            self.browser_mode = BrowserMode.SauceSingle
        else:
            if usecmdline_browser_sauceformat:
                print '(BrowserData)[init] ENV Intersected: [none] (Sauce Solo) mode enabled'
                self.browser_mode = BrowserMode.SauceSolo
            else: #self.usecmdline_browser_localformat
                print '(BrowserData)[init] ENV Intersected: [none] (Local Solo) mode enabled'
                self.browser_mode = BrowserMode.LocalSolo
        
        # parse and store urls
        if self.browser_mode == BrowserMode.SauceMultiple:
            self.raw_json = json.loads(os.environ.get('SAUCE_ONDEMAND_BROWSERS')) 
            for browser_item in self.raw_json:            
                if 'url' in browser_item:
                    self.url_list.append(browser_item['url'])                    
        elif self.browser_mode == BrowserMode.SauceSingle:
            self.url_list.append(os.environ.get('SELENIUM_DRIVER'))            
        elif self.browser_mode == BrowserMode.LocalSolo:
            default_url = config.DEFAULT_SAUCEURL % (os.getenv('SAUCE_USERNAME', config.SAUCE_USERNAME), os.getenv('SAUCE_ACCESSKEY', config.SAUCE_ACCESSKEY), 'Windows 2012 R2', config.DEFAULT_SOLO_BROWSER, '11')
            self.url_list.append(default_url)
        else: #SauceSolo
            _os, _browser, _version = os.environ.get('BROWSER').split(',')
            default_url = config.DEFAULT_SAUCEURL % (os.getenv('SAUCE_USERNAME', config.SAUCE_USERNAME), os.getenv('SAUCE_ACCESSKEY', config.SAUCE_ACCESSKEY), _os, _browser, _version)
            self.url_list.append(default_url)
        # use overrides in place of the urls            
        for i, url_item in enumerate(self.url_list):
            # if usecmdline_username:
                # url_item['username'] = os.environ.get('SAUCE_USERNAME') 
            # if usecmdline_accesskey:
                # url_item['access-key'] = os.environ.get('SAUCE_ACCESSKEY') 
            if self.usecmdline_browser_localformat:
                fields = self.getUrlHash(i)                
                fields['browser'] = os.environ.get('BROWSER')
                self.setUrlHash(fields, i)
            #if usecmdline_browser_sauceformat:self.getUrlHash(i) 
                # os=Linux&browser=chrome&browser-version=32
                # Linux,chrome,32
                # url_item['os'],url_item['browser'],url_item['browser-version'] = os.environ.get('BROWSER').split(',')
    
    def setRuntimeENV(self, i, config, test_name):
        if not self.usecmdline_base_url:
            os.environ['BASE_URL'] = config.BASE_URL   
        if self.usecmdline_browser_localformat:
            os.environ["PYBROWSER"] = self.getBrowser(i)
        os.environ["PYROBOT_REMOTE_URL"] = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (self.getUserName(i), self.getAccessKey(i))
        #os.environ["PYROBOT_CAPS"] = 'name:%s,platform:%s,version:%s,browserName:%s,javascriptEnabled:True' % (test_name, self.getOS(i), self.getBrowserVersion(i), self.getBrowser(i))
        os.environ["PYROBOT_CAPS"] = config.BROWSER_CAPABILITIES % (test_name, self.getOS(i), self.getBrowserVersion(i), self.getBrowser(i))   

if not self.usecmdline_display:
            os.environ['DISPLAY'] = config.DEFAULT_BROWSER_DISPLAY          
        
        print '(BrowserData)[setRuntimeENV] BASE_URL:            %s' %  os.environ['BASE_URL']
        print '(BrowserData)[setRuntimeENV] PYROBOT_REMOTE_URL:  %s' %  os.environ['PYROBOT_REMOTE_URL']
        print '(BrowserData)[setRuntimeENV] PYROBOT_CAPS:        %s' %  os.environ['PYROBOT_CAPS']
        print '(BrowserData)[setRuntimeENV] DISPLAY:             %s' %  os.environ['DISPLAY']
    
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
   
    def setUrlHash(self, fields, index):         
        new_url = ""
        new_url_items = []
        for key, value in fields.items():
            new_url_items.append("%s=%s" % (key, value))
        new_url = "sauce-ondemand:?" + '&'.join(new_url_items)
        self.url_list[index] = new_url
        
    def getValue(self, target_key, index):   
        fields = self.getUrlHash(index)
        if target_key in fields:
            return fields[target_key]
        else:
            return None

    def getBrowser(self, index):
        return self.getValue("browser", index)
            
    def getOS(self, index):
        if self.browser_mode == BrowserMode.LocalSolo:
            return platform.system() 
        else:
            return self.getValue("os", index)

    def getBrowserVersion(self, index):        
        if self.browser_mode == BrowserMode.LocalSolo:
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
            