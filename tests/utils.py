import os
import shutil
import sys
import unittest

if sys.version_info < (3, 5):
    # noinspection PyUnresolvedReferences
    # python <= 3.4 backport (mkdir exist_ok param is from py35)
    from pathlib2 import Path
else:
    from pathlib import Path


class TempDirTestCase(unittest.TestCase):
    def setUp(self):
        self.TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
        Path(self.TEMP_DIR).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.TEMP_DIR, ignore_errors=True)
