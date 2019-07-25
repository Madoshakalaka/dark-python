import os
import subprocess
import sys
import unittest
from os import path

from gapp import main


class MyTestCase(unittest.TestCase):
    oldDir = ""

    def setUp(self) -> None:
        MyTestCase.oldDir = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_stuff(self):
        pass


    def tearDown(self) -> None:

        os.chdir(MyTestCase.oldDir)

if __name__ == '__main__':
    unittest.main()
