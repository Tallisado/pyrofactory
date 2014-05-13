import unittest
import sys

sys.path.append("../")
sys.path.append("../../")
from src.pyro_factory.robot_results_parser import ConstructEmailResults


class TestConstructEmailResults(unittest.TestCase):

    def setUp(self):
        self.parser = ConstructEmailResults()

    def testMessageCreate(self):
        email_type = 'weekly'        
        example = 'example_weekly'        
        msg = "Automation Summary:\n\n"         

        constructed_email_results = ConstructEmailResults(example) 

        msg += "\n\nTotal tests: %s\n" % (sum(pyro_result.suite_test_count for pyro_result in constructed_email_results.pyro_results))

        for i, pyro_result in enumerate(constructed_email_results.pyro_results):
            msg += "  %s(%s)\r\n" % (pyro_result.get_name(email_type), pyro_result.suite_test_count)

        msg += "\nResults that have (FAILED):\n"
        for pyro_result in constructed_email_results.pyro_results:
            if not pyro_result.test_statuses_passed():    
                msg += "  %s\r\n" % (pyro_result.get_name(email_type))

        msg += "\n\nResults that have (PASSED):\n"
        for pyro_result in constructed_email_results.pyro_results:
            if pyro_result.test_statuses_passed():    
                msg += "  %s\r\n" % (pyro_result.get_name(email_type))
                
        if 'TEAMCITY_VERSION' in os.environ:
            artifacts_weblink = "http://10.10.8.17/teamcity/viewLog.html?buildId=%s&buildTypeId=%s&tab=artifacts" % (os.environ.get('BUILDID', '0'), os.environ.get('BUILDTYPEID', '0'))
            buildlog_weblink = "http://10.10.8.17/teamcity/viewLog.html?buildId=%s&buildTypeId=%s&tab=buildLog" % (os.environ.get('BUILDID', '0'), os.environ.get('BUILDTYPEID', '0'))
            #artifacts_weblink = "http://10.10.8.17/teamcity/viewLog.html?buildId=%s&buildTypeId=%s&tab=artifacts" % ('2829', 'WeeklyDev_03SauceSingleV11') # buildId, buildTypeId
            email_message += "\n  TeamCity Artifacts: \n   %s" % artifacts_weblink        
            email_message += "\n  TeamCity BuildLogs: \n   %s" % buildlog_weblink        

        msg += "\n\nDetailed Failure Results:\n"    
        for pyro_result in constructed_email_results.pyro_results:
            for i, status in enumerate(pyro_result.test_statuses):
               if pyro_result.test_statuses[i] != 'PASS':
                   msg += "(%s) %s | %s\n" % (pyro_result.get_name(email_type), pyro_result.test_names[i], pyro_result.fail_messages[i])    
            
        print "-----------------"
        print msg
        print "-----------------"
   

if __name__ == "__main__":
    unittest.main()
