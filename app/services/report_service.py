# from flask import current_app
from app.exceptions.CustomExceptions import ServiceException
from app.repositories.reporting_repository import repo_process_property_data


def process_property_data(page, page_size):
    report = repo_process_property_data()

    if not report:
        raise ServiceException("There was an issues with the reporting processing service. Please try again.")
    
    # Calculate start and end indices for the current page (starts a zero index)
    start = (page - 1) * page_size
    end = start + page_size

    report_page = report[start:end]

    total_count = len(report)

    return (report_page, total_count)
