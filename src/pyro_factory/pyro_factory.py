 #BASE_URL=http://10.10.9.63 BROWSER='Linux,chrome,32' PAYLOAD=/mnt/wt/pyrobot_2/pyrobot/dev/spec/02__pyrobot_library.txt python pyrobot.py
 #BASE_URL=http://10.10.9.63 BROWSER='chrome' PAYLOAD=/mnt/wt/pyrobot_2/pyrobot/dev/spec/02__pyrobot_library.txt python pyrobot.py
 #WORKSPACE_UID=WEEKLY_DEV_%env.BUILD_NUMBER% BASE_URL=http://10.10.9.63 BROWSER='Linux,chrome,32' PAYLOAD=/mnt/wt/pyrobot_2/pyrobot/dev/spec/02__pyrobot_library.txt python /mnt/wt/pyrobot_2/pyrobot/pyrobot.py
 
# imports
# from robot.running import TestSuite
# from robot import utils
# from robot.conf import settings
import os, glob
import subprocess
import time
from datetime import datetime
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
#foo = imp.load_source('browser_data', '/mnt/wt/pyrobot_2/pyrofactory/src/pyro_factory/browser_data.py')
#from sauce_rest import *
 
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
   
    def start(self, payload, workspace_home, client_cwd, typology, args=[]):
        """ Starts the pybot script from RobotFramework executing the given 'suite'.
        'args' (optional) is a list of additional parameters passed to pybot
        """
        self.payload = payload
        self.output_file = '%s_Output.xml' % self.name
        self.log_file = '%s_Log.html' % self.name 
        self.report_file = '%s_Report.html' % self.name

        self.py_runner_log = os.path.join(workspace_home, ("%s_Stdout.txt" % self.name))
        jyLog = open(self.py_runner_log, "w")        
        #jybotCommand = "pybot %s --name %s --outputdir %s --output %s --log %s --report %s %s" % (typology, self.name, workspace_home, self.output_file, self.log_file, self.report_file, payload)
        jybotCommand = "pybot --name %s --outputdir %s --output %s --log %s --report %s %s" % (self.name, workspace_home, self.output_file, self.log_file, self.report_file, payload)
        
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
            #typology = "--variablefile %s" % os.path.join(os.path.realpath("./") ,os.environ.get('TYPOLOGY', self._config.DEFAULT_TYPOLOGY))
            typology = ""
            os.environ['ONDEMAND_PYRO'] = "PLACEHOLDER_ONDEMAND_STRING"
        except:
            raise
            usage()
            sys.exit(2)
        
        # save current time to calculate execution time at the end of the script
        startTime = datetime.now()
        
        # reading variables from ParabotConfig
        time_between_test_start_up = self._config.time_between_test_start_up
        
        # runtime variables
        base_dir = "./"
        pybots = []
        suite_name = os.path.basename(os.path.normpath(relative_payload))
        client_cwd = os.path.realpath(base_dir) 
    #####    workspace_home = os.path.join(os.path.join(client_cwd, self._config.WORKSPACE), (''.join(random.choice(string.ascii_uppercase) for i in range(12))))
        uid = os.environ.get("WORKSPACE_UID", ''.join(random.choice(string.ascii_uppercase) for i in range(12)))
        workspace_home = os.path.join("/mnt/wt/pyrobot_2/pyrobot/workspace/", uid)
        absolute_payload = os.path.join(os.path.realpath(base_dir), relative_payload)
        
        print '(PyroFactory)[run][RUNTIME] Suite Name:       %s' % suite_name
        print '(PyroFactory)[run][RUNTIME] Client CWD:       %s' % client_cwd
        print '(PyroFactory)[run][RUNTIME] Workspace Home:   %s' % workspace_home
        print '(PyroFactory)[run][RUNTIME] relative_payload: %s' % relative_payload
        print '(PyroFactory)[run][RUNTIME] absolute_payload: %s' % absolute_payload
        
        if not os.path.exists(absolute_payload):
            print '(PyroFactory) [run] payload absolute path must exist! '
            usage()
            sys.exit(2)
        
        # start working
        os.mkdir(workspace_home, 0755)
        for browser_index in range(0, browser_data.getUrlCount()):
            test_name = ("%s_%s_%s" % (browser_data.getBrowser(browser_index), browser_data.getOS(browser_index), browser_data.getBrowserVersion(browser_index))).replace(' ', '_')
            print ""   
            print '(PyroFactory)[run] Starting runner for test:\n[-------] %s' % test_name
            browser_data.setRuntimeENV(browser_index, self._config, test_name)
            runner = PyRunner(test_name)
            #bot = runner.start(absolute_payload, typology, self.getDynArgs(0))
            bot = runner.start(absolute_payload, workspace_home, client_cwd, typology)
            while runner.isRunning():
                time.sleep(time_between_test_start_up)
            pybots.append(bot)
            with open(runner.py_runner_log, 'r') as fin:
                print fin.read()
        
        #print out the OnDemand string for teamcity
        print os.environ.get('ONDEMAND_PYRO')

        
        report = os.path.join(workspace_home, "%s_Report.html" % suite_name)
        log = os.path.join(workspace_home, "%s_Log.html" % suite_name)
        reportRC = self.generateReportAndLog(workspace_home, report, log, suite_name) 
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
        
    def usage():
        """ Prints usage information for Parabot """
        print ""
        print "Usage: python parabot.py [options] <testsuite.tsv>"
        print ""
        print "<testsuite.tsv> can be absolute or relative path + filename of a testsuite."
        print "The containing folder will be used as working directory"
        print ""
        print "Options:"
        print "-h\t--help\t\tThis screen"
        print "-i\t--include\tInclude a tag"
        print "-e\t--exclude\tExclude a tag"
        print "-f\t--forceserial\tForces serial test execution"
        print "-b\t--basedir\tSet parabots base dir"
        print ""
        
    def generateReportAndLog(self, workspace_home, report_file, log_file, report_title):
        """ Calls RobotFrameworks rebot tool to generate Report and Log files from output.xml files
        'xmlFiles' is a list of output.xml files from jybot / pybot
        'report_file' is the path+name of the report.html file to be written
        'log_file' is the path+name of the log.html file to be written
        the global variable 'payload' will be used a report title
        """    
        rebotCommand = "rebot --log %s --report %s --reporttitle \"%s\" --name ' ' %s/*.xml" % (log_file, report_file, report_title, workspace_home)      
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