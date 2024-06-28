from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_cors import CORS
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

# database set up
db = SQLAlchemy(metadata=metadata)

# initialise other Flask extensions
migrate = Migrate()
# api = Api()
# cors = CORS()