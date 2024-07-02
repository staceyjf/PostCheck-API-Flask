# from flask import current_app
from app.exceptions.CustomExceptions import ServiceException
from app.repositories.reporting_repository import repo_process_property_data


def process_property_data():
    report = repo_process_property_data()

    if not report:
        raise ServiceException("There was an issues with the reporting processing service. Please try again.")

    colours = {
        "ACT": "hsl(24, 100%, 50%)",  # Orange
        "NSW": "hsl(120, 60%, 50%)",  # Green
        "VIC": "hsl(200, 70%, 50%)",  # Blue
        "QLD": "hsl(340, 80%, 50%)",  # Pink
        "SA": "hsl(60, 70%, 50%)",    # Yellow
        "WA": "hsl(280, 50%, 50%)",   # Purple
        "TAS": "hsl(0, 100%, 50%)",   # Red
        "NT": "hsl(30, 100%, 50%)"    # Brown
    }

    # shape of data needed for Nivo
    # {{
    #     "id": "japan",
    #     "color": "hsl(45, 70%, 50%)",
    #     "data": [
    #       {
    #         "x": 0,
    #         "y": 37
    #       },
    #              ]
    # }}
    chartObjects = []  # [{},{}]
    ids_seen = set()

    for item in report:
        id = item.state
        if id not in ids_seen:
            # If id not seen, create new dict
            reportObj = {"id": id, "color": colours[id], "data": []}
            chartObjects.append(reportObj)
            ids_seen.add(id)

        # Find the correct datapoint to append the new data
        for datapoint in chartObjects:
            if datapoint["id"] == id:
                chartPoint = {"y": item.avg_price, "x": item.date_sold}
                datapoint["data"].append(chartPoint)
                break   # break the loop once the datapoint has been updated

    return chartObjects
