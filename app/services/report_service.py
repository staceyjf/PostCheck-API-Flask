from flask import current_app
from app.exceptions.CustomExceptions import ServiceException
import json
import os


def process_property_data():
    try:
        # Task: review a better way to do this
        data_file_path = os.path.join(current_app.root_path, 'data', 'avg_price_by_state.json')

        # Open and read the data from the file
        with open(data_file_path, "r") as chart_data:
            data = json.load(chart_data)  # convert into a dict
            return data
    except FileNotFoundError as e:
        raise ServiceException(f"The file was not found: {e}")
    except OSError as e:
        raise ServiceException(f"There was an issue with reading the file: {e}")
