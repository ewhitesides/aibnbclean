import os
import json
from typing import Any


def get_json_file_data(filepath: str) -> Any:
    if not (filepath):
        raise ValueError(
            f"filepath parameter is required"
        )

    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"{filepath} does not exist"
        )

    with open(filepath, 'r') as file:
        output = json.load(file)
        return output
