import unittest
from aibnbclean.process import process


class TestProcess(unittest.TestCase):

    def test_process(self):
        """
        test that process function runs without error
        """
        process()
