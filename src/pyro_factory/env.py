import os
import sys

WORKSPACE_HOME = os.path.join("/mnt/wt/pyrobot/workspace/", ''.join(random.choice(string.ascii_uppercase) for i in range(12)))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UNIT_TEST_DIR = os.path.join(ROOT_DIR, "unit")
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, "acceptance")
LIB_DIR = os.path.join(ROOT_DIR, "lib")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
HTTP_SERVER_FILE = os.path.join(RESOURCES_DIR, 'testserver', 'testserver.py')
SRC_DIR = os.path.join(ROOT_DIR, "..", "src")

sys.path.insert(0, SRC_DIR)
sys.path.append(LIB_DIR)
sys.path.append(UNIT_TEST_DIR)