import os
from dotenv import load_dotenv
from .AirbnbBrowser import AirbnbBrowser


def login() -> None:

    load_dotenv()

    config_dir = os.environ["AIBNBCLEAN_CONFIG_DIR"]

    if not config_dir:
        raise ValueError("AIBNBCLEAN_CONFIG_DIR environment variable is not set")

    browser_headless = False
    browser_user_data_dir = f"{config_dir}/browser_profile"

    with AirbnbBrowser(
        headless=browser_headless, user_data_dir=browser_user_data_dir
    ) as browser:

        logged_in = browser.is_logged_in()

        if logged_in:
            print("Already logged in to Airbnb, exiting.")
            return
        else:
            print("Not logged in to Airbnb, opening browser for login.")
            browser.login()
