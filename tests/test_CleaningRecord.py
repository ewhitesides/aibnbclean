import os
from dotenv import load_dotenv
from aibnbclean.get_json_file_data import get_json_file_data
from aibnbclean.get_gcal_entries import get_gcal_entries
from aibnbclean.AirbnbBrowser import AirbnbBrowser
from aibnbclean.CleaningRecord import CleaningRecord
import unittest


class TestCleaningRecord(unittest.TestCase):

    def test_cleaning_record(self):
        """
        test that CleaningRecord class can be instantiated without error and has expected attributes
        """
        load_dotenv()

        config_dir = os.environ["AIBNBCLEAN_CONFIG_DIR"]

        listings = get_json_file_data(filepath=f"{config_dir}/listings.json")
        listing = listings[0]

        browser_headless = False
        browser_user_data_dir = f"{config_dir}/browser_profile"

        with AirbnbBrowser(
            headless=browser_headless, user_data_dir=browser_user_data_dir
        ) as ab:

            gcal_entries = get_gcal_entries(
                url=listing["url"], type=listing["type"], qty=10
            )
            self.assertIsInstance(gcal_entries, list)

            gcal_entry = gcal_entries[1]

            cr = CleaningRecord.from_gcal_ab_reservation(
                gcal_entry,
                listing["name"],
                listing["type"],
                listing["default_cleaning_fee"],
                listing["laundry"],
            )

            self.assertIsInstance(cr, CleaningRecord)

            self.assertTrue(ab.is_logged_in())

            page = ab.get_new_page()

            cr.set_message_url(page)
            self.assertIsNotNone(cr.message_url)

            cr.set_message_text(page)
            self.assertIsNotNone(cr.message_text)

            cr.set_guest_name_qty(page)
            self.assertIsNotNone(cr.guest_name)
            self.assertNotEqual(cr.guest_name, 0)

            # test set_cleaning_fee method by setting cleaning_fee to 0
            # and then calling the method to update it
            cr.cleaning_fee = 0
            cr.set_cleaning_fee(page)
            self.assertNotEqual(cr.cleaning_fee, 0)
