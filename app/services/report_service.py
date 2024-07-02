# from flask import current_app
from app.exceptions.CustomExceptions import ServiceException
from app.repositories.reporting_repository import repo_process_property_data


def process_property_data():
    report = repo_process_property_data()

    if not report:
        raise ServiceException("There was an issues with the reporting processing service. Please try again.")

    # current_app.logger.info(f"repo_process_property_data is sending back {report}")

    return report
