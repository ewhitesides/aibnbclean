import unittest
from login import login


class TestLogin(unittest.TestCase):

    def test_login(self):
        """
        test that login function runs without error
        """
        login()
