from sqlalchemy import select
from app.extensions import db
from app.models.models import PostCode

class PostcodeRepository:
    def get_all_postcodes(self):
        return PostCode.query.all()