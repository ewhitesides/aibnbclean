import os
from dotenv import load_dotenv
from .get_json_file_data import get_json_file_data
from .process_ab_listing import process_ab_listing
from .process_home_listing import process_home_listing
from .get_json_file_data import get_json_file_data
from .AirbnbBrowser import AirbnbBrowser


def process():

    load_dotenv()

    config_dir = os.environ["AIBNBCLEAN_CONFIG_DIR"]

    if not config_dir:
        raise ValueError("AIBNBCLEAN_CONFIG_DIR environment variable is not set")

    secrets = get_json_file_data(filepath=f"{config_dir}/secrets.json")

    listings = get_json_file_data(filepath=f"{config_dir}/listings.json")

    browser_headless = os.environ["AIBNBCLEAN_HEADLESS"] in ["1"]

    browser_user_data_dir = f"{config_dir}/browser_profile"

    for listing in listings:
        if listing["type"] == "airbnb":
            with AirbnbBrowser(
                headless=browser_headless, user_data_dir=browser_user_data_dir
            ) as browser:
                try:
                    process_ab_listing(listing, secrets, browser)
                except Exception as e:
                    print(f"error processing listing {listing['name']}: {e}")

        if listing["type"] == "home":
            try:
                process_home_listing(listing, secrets)
            except Exception as e:
                print(f"error processing listing {listing['name']}: {e}")
