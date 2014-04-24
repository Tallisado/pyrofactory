 #BASE_URL=http://10.10.9.63 BROWSER='Linux,chrome,32' PAYLOAD=/mnt/wt/pyrobot_2/pyrobot/dev/spec/02__pyrobot_library.txt python pyrobot.py
 #BASE_URL=http://10.10.9.63 BROWSER='chrome' PAYLOAD=/mnt/wt/pyrobot_2/pyrobot/dev/spec/02__pyrobot_library.txt python pyrobot.py
 #WORKSPACE_UID=WEEKLY_DEV_%env.BUILD_NUMBER% BASE_URL=http://10.10.9.63 BROWSER='Linux,chrome,32' PAYLOAD=/mnt/wt/pyrobot_2/pyrobot/dev/spec/02__pyrobot_library.txt python /mnt/wt/pyrobot_2/pyrobot/pyrobot.py
 
# imports
# from robot.running import TestSuite
# from robot import utils
# from robot.conf import settings
from robot.api import ExecutionResult
import os, glob
import subprocess
import time
from datetime import datetime
from xml.dom import minidom
import sys
# import getopt
# import fileinput
import random
import string
import random
import shutil

#import pyrobot_config as config
###from browser_data import *
import imp
from browser_data import BrowserData
from robot_results_parser import RobotResultsParser
#foo = imp.load_source('browser_data', '/mnt/wt/pyrobot_2/pyrofactory/src/pyro_factory/browser_data.py')
#from sauce_rest import *

# send_mail    
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
 
class PyRunner():
    """ Helper class to interact with RobotFrameworks pybot script to execute tests / test suites.    
    """
    name = ""
    args = []
    process = -1
    running = False
    py_runner_log = ""
   
    def __init__(self, name):
        """ Constructor, creates the object and assigns the given 'name'.
        """
        self.name = name
   
    def start(self, payload, working_directory, client_cwd, pybot_argstring, args=[]):
        """ Starts the pybot script from RobotFramework executing the given 'suite'.
        'args' (optional) is a list of additional parameters passed to pybot
        """
        self.payload = payload
        self.output_file = '%s_Output.xml' % self.name
        self.log_file = '%s_Log.html' % self.name 
        self.report_file = '%s_Report.html' % self.name

        self.py_runner_log = os.path.join(working_directory, ("%s_Stdout.txt" % self.name))
        jyLog = open(self.py_runner_log, "w")        
        jybotCommand = "pybot %s --name %s --outputdir %s --output %s --log %s --report %s %s" % (pybot_argstring, self.name, working_directory, self.output_file, self.log_file, self.report_file, payload)
        #jybotCommand = "pybot --name %s --outputdir %s --output %s --log %s --report %s %s" % (self.name, working_directory, self.output_file, self.log_file, self.report_file, payload)
        
        print "(PyroFactory,PyRunner)[start] Starting the following pybot instance:\n[-------] %s ..." % jybotCommand
        self.running = True
        #self.process = subprocess.Popen(["pybot", "-o", "%s" % os.path.join(log_folder, self.output_file), "%s" % self.suite], cwd=client_cwd, stdout=jyLog, stderr=jyLog)
        self.process = subprocess.Popen(jybotCommand.split(' '), cwd=client_cwd, stdout=jyLog, stderr=jyLog)
   
    def isRunning(self):
        """ Polls the pybot subprocess to check if it's running. Will return true if the process is running.
        Returns false if the process hasn't been started or has finished already.
        """
        if not self.running:
            return False
        elif self.process.poll() == 0 or self.process.returncode >= 0:
            return False
        else:
            return True
   
    def stop(self):
        """ Kills the pybot subprocess.
        """
        os.system("taskkill /T /F /PID %s" % self.process.pid)
        self.running = False
        
######################################################################################################
class PyroFactory():
    def __init__(self):
        print '(PyroFactory) ----------------> ........ <-----------------'
        print '(PyroFactory) ----------------> Starting <-----------------'
        print '(PyroFactory) ----------------> ........ <-----------------'
        pass
        
    def run(self,config):
        self._config = config
        try:
            browser_data = BrowserData(self._config)
            if 'PAYLOAD' in os.environ:
                relative_payload = os.environ.get('PAYLOAD')
            else:
                raise NameError('(PyroFactory)[run] RUNTIME ERROR: PAYLOAD is a mandatory environment variable')
            os.environ['ONDEMAND_PYRO'] = "PLACEHOLDER_ONDEMAND_STRING"
        except:
            raise
            self.usage()
            sys.exit(2)
        
        # save current time to calculate execution time at the end of the script
        startTime = datetime.now()
        
        # reading variables from ParabotConfig
        time_between_test_start_up = self._config.time_between_test_start_up
        
        # runtime variables
        base_dir = "./"
        pybots = []
        
        suite_name = os.path.basename(os.path.normpath(relative_payload))
        if '.' in suite_name:
            suite_name = os.path.splitext(suite_name)[0]
            
            
        client_cwd = os.path.realpath(base_dir) 
    #####    workspace_home = os.path.join(os.path.join(client_cwd, self._config.WORKSPACE), (''.join(random.choice(string.ascii_uppercase) for i in range(12))))
        uid = os.environ.get("WORKSPACE_UID", ''.join(random.choice(string.ascii_uppercase) for i in range(12)))
        workspace_home = os.path.join(self._config.WORKSPACE_HOME, uid)
        testspace_home = os.path.join(workspace_home, suite_name)
        absolute_payload = os.path.join(os.path.realpath(base_dir), relative_payload)
        
        pyarg_variable_file = os.path.join(self._config.DEFAULT_TOPOLOGY_FOLDER, self._config.DEFAULT_TOPOLOGY)
        pybot_argstring = "--variablefile %s" % pyarg_variable_file
                
        print '(PyroFactory)[run][RUNTIME] Suite Name:       %s' % suite_name
        print '(PyroFactory)[run][RUNTIME] Client CWD:       %s' % client_cwd
        print '(PyroFactory)[run][RUNTIME] Workspace Home:   %s' % workspace_home
        print '(PyroFactory)[run][RUNTIME] Testspace Home:   %s' % testspace_home
        print '(PyroFactory)[run][RUNTIME] relative_payload: %s' % relative_payload
        print '(PyroFactory)[run][RUNTIME] absolute_payload: %s' % absolute_payload
        
        if not os.path.exists(absolute_payload):
            print '(PyroFactory) [run] payload absolute path must exist! '
            self.usage()
            sys.exit(2)
        
        # start working
        os.makedirs(testspace_home, 0755)
        
        for browser_index in range(0, browser_data.getUrlCount()):
            test_name = ("%s_%s_%s" % (browser_data.getBrowser(browser_index), browser_data.getOS(browser_index), browser_data.getBrowserVersion(browser_index))).replace(' ', '_')
            print ""   
            print '(PyroFactory)[run] Starting runner for test:\n[-------] %s' % test_name
            browser_data.setRuntimeENV(browser_index, self._config, test_name)
            runner = PyRunner(test_name)
            #bot = runner.start(absolute_payload, typology, self.getDynArgs(0))
            bot = runner.start(absolute_payload, testspace_home, client_cwd, pybot_argstring)
            while runner.isRunning():
                time.sleep(time_between_test_start_up)
            pybots.append(bot)
            with open(runner.py_runner_log, 'r') as fin:
                print fin.read()
        
        #print out the OnDemand string for teamcity
        print os.environ.get('ONDEMAND_PYRO')

        
        # output = os.path.join(testspace_home, "%s_OUTPUT.xml" % suite_name)
        # report = os.path.join(testspace_home, "%s_REPORT.html" % suite_name)
        # log = os.path.join(testspace_home, "%s_LOG.html" % suite_name)      
        
        output = "%s_OUTPUT.xml" % suite_name
        report = "%s_REPORT.html" % suite_name
        log = "%s_LOG.html" % suite_name
        
        reportRC = self.generateReportAndLog(workspace_home, output, log, report, " ", suite_name) 
        #send_email(testspace_home, workspace_home, output
        
        # delete XML output files after generating the report / log (if report generation
        # returned zero)
        #if reportRC == 0:
        #    for outXML in outputXmls:
        #        os.remove(outXML)
        
        execution_time = datetime.now() - startTime
        print ""
        print "(PyroFactory) [Execution Time]: %s" % execution_time        
        print '(PyroFactory) ----------------> ......... <-----------------'
        print '(PyroFactory) ----------------> Finishing <-----------------'
        print '(PyroFactory) ----------------> ......... <-----------------'
      
    def send_email(self, workspace_home):
        #verbose_stream = sys.stdout
        print "(PyroFactory) [send_email]: Email Results"        

        # determine if this is weekly or nightly
        email_type = os.environ.get('TEAMCITY_PROJECT_NAME', 'Unknown')
        if 'nightly' in email_type:
            email_type = 'Nightly'
        elif 'weekly' in email_type:
            email_type = 'Weekly'
            
        email_message = "Automation Summary:\n\n"        
        
        verbose_stream = None
        rrp = RobotResultsParser(False, verbose_stream)
        robot_results = []
        #working_dir = '/mnt/wt/pyrobot_v1.1/pyrobot/workspace/tester'
        for dirname in os.walk(workspace_home).next()[1]:
            print dirname
            test_dir = os.path.join(workspace_home,dirname)
            for file in os.listdir(test_dir):
                if file.endswith(".xml"):
                    print file
                    robot_results.append(rrp.xml_to_object(os.path.join(test_dir,file), dirname))
 
        suite_result = "PASSED"
        for result in robot_results:           
            if result.failed == 0:
                task_text_result = "PASSED"
            else:
                task_text_result = "FAILED"
                suite_result = "FAILED"
                
            if email_type == 'Nightly':
                email_message += "  %10s -> %10s\n" % (result.suite, task_text_result)
            else:
                email_message += "  %10s   %-40s -> %10s\n" % (result.suite, os.path.basename(os.path.normpath(result.source))[:-11], task_text_result)
        
        #http://10.10.8.17/teamcity/viewLog.html?buildId=2829&buildTypeId=WeeklyDev_03SauceSingleV11&tab=artifacts
        #echo "##teamcity[setParameter name='env.BUILDID' value='%teamcity.build.id%']"
        #echo "##teamcity[setParameter name='env.BUILDTYPEID' value='%system.teamcity.buildType.id%']"        
        if 'BUILDID' in os.environ and 'BUILDTYPEID' in os.environ:
            artifacts_weblink = "http://10.10.8.17/teamcity/viewLog.html?buildId=%s&buildTypeId=%s&tab=artifacts" % ('2829', 'WeeklyDev_03SauceSingleV11') # buildId, buildTypeId
            email_message += "\n   TeamCity Artifacts: \n   %s" % artifacts_weblink
                
        print email_message
        
        msg = MIMEText(email_message,"\n\n")
        
        me = 'talliskane@gmail.com' 
        you = 'tallis.vanek@adtran.com'

        msg['Subject'] = "<%s %s>" % (email_type, suite_result)
        msg['From'] = me
        msg['To'] = you

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
    
    def usage():
        """ Prints usage information for PyroFactory """
        print ""
        print "Usage: python pyrobot.py [options] <testsuite_dir|testfile.txt>"
        print ""
        print "<testsuite|testfile> can be absolute or relative path OR filename of testcode."
        print "The containing folder will be used as working directory"
        print ""
        # print "Options:"
        # print "-h\t--help\t\tThis screen"
        # print "-i\t--include\tInclude a tag"
        # print "-e\t--exclude\tExclude a tag"
        # print "-f\t--forceserial\tForces serial test execution"
        # print "-b\t--basedir\tSet parabots base dir"
        # print ""
        # TODO: WRITE A BETTER USAGE !!
        
    def generateReportAndLog(self, workspace_folder, output_file, log_file, report_file, report_title, name):
        """ Calls RobotFrameworks rebot tool to generate Report and Log files from output.xml files
        """    
        rebot_payload = '%s/**/*.xml' % workspace_folder
        rebotCommand = "rebot --outputdir %s --output %s --log %s --report %s --reporttitle '%s' --name '%s' %s" % (workspace_folder, output_file, log_file, report_file, report_title, name, rebot_payload)      
        print "(PyroFactory) [generateReportAndLog]: Rebot Consolidation "       
        print "(PyroFactory,generateReportAndLog) Starting the following rebot instance:-------> %s" % rebotCommand     
        rc = os.system(rebotCommand)
        return rc

    def getDynArgs(index):
        """ Reads the DYN_ARGS variable from the config file and parses it into a list of argument strings
        like --variable name:"value".
        This list can be passed to the Pybot start() method as args[] list.
        """
        arglist = []
        for row in _config.DYN_ARGS:
            valueIndex = index
            if len(row) < 2:
                print "Error reading DYN_ARGS: Row is invalid: %s. Row will be skipped!" % row
            else:
                varName = row[0]
                values = []
                i = 1
                while i < len(row):
                    values.append(row[i])
                    i = i+1
                if valueIndex >= len(values):
                    valueIndex = (len(values)-1) % valueIndex
                varValue = values[valueIndex]
                arglist.append("--variable %s:\"%s\"" % (varName, varValue))
        return arglist