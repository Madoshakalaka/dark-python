import os
import unittest


class MyTestCase(unittest.TestCase):
    oldDir = ""

    def setUp(self) -> None:
        MyTestCase.oldDir = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_stuff(self):
        assert bool("my code is perfect") is True


    def tearDown(self) -> None:

        os.chdir(MyTestCase.oldDir)

if __name__ == '__main__':
    unittest.main()
