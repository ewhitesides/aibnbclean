import os
from dotenv import load_dotenv
from .AirbnbBrowser import AirbnbBrowser


def login() -> None:

    load_dotenv()

    config_dir = os.environ["AIBNBCLEAN_CONFIG_DIR"]

    if not config_dir:
        raise ValueError(
            "AIBNBCLEAN_CONFIG_DIR environment variable is not set"
        )

    ab = None

    try:
        ab = AirbnbBrowser(headless=False)
        logged_in = ab.is_logged_in()

        if logged_in:
            print("Already logged in to Airbnb, exiting.")
            return
        else:
            print("Not logged in to Airbnb, opening browser for login.")
            ab.login()

    finally:
        if ab:
            ab.close()
