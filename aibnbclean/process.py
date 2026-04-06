import os
from dotenv import load_dotenv
from .get_json_file_data import get_json_file_data
from .process_ab_listing import process_ab_listing
from .process_home_listing import process_home_listing


def process():

    load_dotenv()

    config_dir = os.environ["AIBNBCLEAN_CONFIG_DIR"]

    if not config_dir:
        raise ValueError(
            "AIBNBCLEAN_CONFIG_DIR environment variable is not set"
        )

    listings = get_json_file_data(
        filepath=f"{config_dir}/listings.json"
    )

    secrets = get_json_file_data(
        filepath=f"{config_dir}/secrets.json"
    )

    for listing in listings:
        if listing['type'] == 'airbnb':
            process_ab_listing(listing, secrets)

    for listing in listings:
        if listing['type'] == 'home':
            process_home_listing(listing, secrets)
