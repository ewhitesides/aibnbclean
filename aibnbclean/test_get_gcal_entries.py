import os
from dotenv import load_dotenv
from get_json_file_data import get_json_file_data
from get_gcal_entries import get_gcal_entries
import unittest


class GetGcalEntries(unittest.TestCase):

    def test_get_cal_entries(self):
        """
        test that get_cal_entries function returns a list of events without error
        """
        load_dotenv()

        config_dir = os.environ["AIBNBCLEAN_CONFIG_DIR"]

        listings = get_json_file_data(
            filepath=f"{config_dir}/listings.json"
        )

        gcal_entries = get_gcal_entries(
            url=listings[0]['url'],
            type=listings[0]['type'],
            qty=1
        )

        self.assertIsInstance(gcal_entries, list)
