import os
from datetime import datetime
from hashlib import sha1
#from robot.api import ExecutionResult
from robot.result.executionresult import CombinedResult
from robot.api import ExecutionResult, ResultVisitor
from robot.errors import DataError


# suite_name        #payload_folder
# suite_test_count
# test_names        #keywords 
#   - status
#   - fail_message


class PyroTestResult():
    def __init__(self):
        self._suite_name = None
        self._caps_name = None
        self._test_names = []
        self._test_statuses = []
        self._fail_messages = []
        self._elapsed_times = []
        self._suite_tests = 0
        
    def empty_testsuite(self, source):
        self.add_fail_message('While running tests an empty suite was returned from robot framework =(')
        self._suite_name = source.rsplit('/', 1)[0]
        self.add_test_status('FAIL')
        self.add_test_name('ERROR')
        return self
                
    #self._suite_name.split('/')[-2]
    @property
    def suite_name(self):
        return self._suite_name
    
    @suite_name.setter
    def suite_name(self, value):
        self._suite_name = value

    @property
    def caps_name(self):
        return self._caps_name
    
    @caps_name.setter
    def caps_name(self, value):
        self._caps_name = value

    @property
    def suite_test_count(self):
        return self._suite_tests    
        
    @suite_test_count.setter
    def suite_test_count(self, value):
        self._suite_tests = value
        
    # def add_suite_test(self, value):
        # self._suite_tests.append(value)
        
    @property
    def test_names(self):
        return self._test_names   
        
    @test_names.setter
    def test_names(self, value):
        self._test_names = value    

    def add_test_name(self, value):
        self._test_names.append(value)          
    
    @property
    def test_statuses(self):
        return self._test_statuses  
        
    @test_statuses.setter
    def test_statuses(self, value):
        self._test_statuses = value   

    def add_test_status(self, value):
        self._test_statuses.append(value)    
            
    @property
    def fail_messages(self):
        return self._fail_messages  

    @fail_messages.setter
    def fail_messages(self, value):
        self._fail_messages = value 

    def add_fail_message(self, value):
        self._fail_messages.append(value)  

    @property
    def elapsed_times(self):
        return self._elapsed_times  
    
    @elapsed_times.setter
    def elapsed_times(self, value):
        self._elapsed_times = value 

    def add_elapsed_time(self, value):
        self._elapsed_times.append(datetime.fromtimestamp(value).strftime('%H:%M:%S.%f'))  

    def test_statuses_passed(self):
        for status in self._test_statuses:
            if status != 'PASS':
                return False
        return True    
    def get_name(self, email_type):
        if 'nightly' in email_type.lower():
            return "%s" % (self.suite_name.split('/')[-1])
        else:
            return "%s (%s)" % (self.caps_name, self.suite_name.split('/')[-1])



class TestResultChecker(ResultVisitor):
    def __init__(self, pyro_test_result):
        self._pyro_test_result = pyro_test_result

    def start_result(self, test):
        #print "START"
        #print test.suite.test_count
        self._pyro_test_result.suite_test_count  = test.suite.test_count
        # print test.suite.source
        self._pyro_test_result.suite_name = test.suite.source
        self._pyro_test_result.caps_name = test.suite.name
        #print test.suite.name
        #print test.suite.longname
        
        
    def visit_test(self, test):        
        self._pyro_test_result.add_test_name(test.name)
        self._pyro_test_result.add_test_status(test.status)
        self._pyro_test_result.add_fail_message(test.message)
        
        #self._pyro_test_result.add_elapsed_time(test.elapsedtime)        
        
        # print test.parent.name
        # print test.name
        # print test.status
                    
    def end_result(self, test):
        # print "END RESULT"
        return self._pyro_test_result

class ConstructEmailResults(object):
    #def __init__(self, workspace_dir, verbose_stream, include_keywords = True):
    def __init__(self, workspace_dir, include_keywords = True):
        #self._verbose = Logger('Parser', verbose_stream)
        self._include_keywords = include_keywords
        self._workspace_dir = workspace_dir
        self._pyro_test_results = []
        
        for dirname in os.walk(self._workspace_dir).next()[1]:    
            testspace_path = os.path.join(os.path.abspath(self._workspace_dir),dirname)
            for xml_file in os.listdir(testspace_path):
                if xml_file.endswith(".xml"):
                    xml_path = (os.path.join(testspace_path,xml_file))
                    #print xml_path
                    try:
                        result = ExecutionResult(xml_path, include_keywords=True)
                    except DataError:
                        print "EMPTY SUITE FOUND, TRYING TO REBOUND: %s " % xml_path
                        self._pyro_test_results.append(PyroTestResult().empty_testsuite(xml_path))
                        #continue
                    else:
                        pyro_result = PyroTestResult()
                        result.visit(TestResultChecker(pyro_result))                        
                        self._pyro_test_results.append(pyro_result)
                    # print "SUITE:" + a.suite_name
                    # print "Test Names"
                    # print a.test_names
                    # print "Test Statuses"
                    # print a.test_statuses
                    # print "Fail Messages"
                    # print a.fail_messages
    @property 
    def pyro_results(self):
        return self._pyro_test_results
    
    # def test_statuses_passed(self, i):
        # print "ASDASD"
        # for status in self._pyro_test_results[i].test_statuses:
            # print status
            # if status != 'PASS':
                # return False
            # return True   