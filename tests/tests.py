import unittest
import subprocess
import time
import xml.etree.ElementTree as ET

# -------------
#   Constants
# -------------

# Timeout after starting Icecast, in seconds
ICECAST_STARTUP_SLEEP = 10

# Timeout after starting DeeFuzzer, in seconds
DEEFUZZER_STARTUP_SLEEP = 5

class IcecastStatusTests(unittest.TestCase):
    """TestCase subclass containing badbackend.core.IcecastStatus test
    items. Runs test Icecast server defined in `test_icecast.xml` and 
    connects with DeeFuzzer instance defined in `test_deefuzzer.yaml`. 
    Note that running these tests will interfere with any unrelated 
    Icecast or DeeFuzzer instances running on the machine!"""

    @classmethod
    def start_icecast():
        """starts backgrounded Icecast instance with config file 
        `test_icecast.xml` using subprocess"""
        subprocess.Popen("icecast -c test_icecast.xml".split())
        print("sleeping after starting Icecast...")
        time.sleep(ICECAST_STARTUP_SLEEP)

    @classmethod
    def stop_icecast():
        """stops Icecast instance using `kill`. This kills the first
        running Icecast instance returned by `pidof icecast` so make
        sure there aren't any important Icecast streams running!"""
        try: 
            icecast_pid = subprocess.check_output("pidof icecast".split())
            subprocess.run(("kill -9 %d" % icecast_pid).split())
        except ValueError:
            # Icecast process not found, presumably already exited
            pass

    @classmethod
    def start_deefuzzer():
        """starts backgrounded DeeFuzzer instance with config file 
        `test_deefuzzer.yaml` using subprocess"""
        subprocess.Popen("deefuzzer test_deefuzzer.yaml".split())
        print("sleeping after starting DeeFuzzer...")
        time.sleep(DEEFUZZER_STARTUP_SLEEP)

    @classmethod
    def stop_deefuzzer():
        """stops DeeFuzzer instance using `kill`. This kills the first
        running DeeFuzzer instance returned by `pidof deefuzzer` so make
        sure there aren't any important DeeFuzzer clients running!"""
        try: 
            deefuzzer_pid = subprocess.check_output("pidof deefuzzer".split())
            subprocess.run(("kill -9 %d" % deefuzzer_pid).split())
        except ValueError:
            # DeeFuzzer process not found, presumably already exited
            pass

    @classmethod
    def setUpClass(cls):
        """Run before tests are begun. Starts Icecast instance defined
        in `test_icecast.xml`"""
        cls.start_icecast()
    
    @classmethod
    def tearDownClass(cls):
        """Run after all tests are complete. Stops Icecast instance"""
        cls.stop_icecast()

    def setUp(self):
        """Run before each test. Loads `test_icecast.xml` config and builds
        IcecastStatus config dict based on it"""
        config_root = ET.parse("test_icecast.xml").getroot()
        self.icecast_config = {
            'server_url':   config_root

    def test_no_show(self):
        
