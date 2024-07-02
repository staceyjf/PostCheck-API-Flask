from app.models.models import Reporting


def repo_process_property_data():
    return Reporting.query.all()
