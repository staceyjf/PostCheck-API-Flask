from app.extensions import db
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import Enum as SQLEnum

# join table for the many-to-many relationship
postcode_suburb_association = Table(
    'postcode_suburb', db.metadata,
    Column('postcode_id', Integer, ForeignKey('postcodes.id')),
    Column('suburb_id', Integer, ForeignKey('suburbs.id'))
)


class PostCode(db.Model):
    __tablename__ = 'postcodes'
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.String(4), nullable=False, unique=True)
    # Define the M:M relationship via the join table with a bi-directional relationship (back_populates)
    associatedSuburbs = relationship("Suburb", secondary=postcode_suburb_association,
                                     back_populates="associatedPostCodes")

    def __str__(self):
        return f"PostCode: {self.postcode}, associatedSuburbs: {self.associatedSuburbs}"


class States(Enum):
    NEW_SOUTH_WALES = 'NSW'
    VICTORIA = 'VIC'
    QUEENSLAND = 'QLD'
    SOUTH_AUSTRALIA = 'SA'
    WESTERN_AUSTRALIA = 'WA'
    TASMANIA = 'TAS'
    NORTHERN_TERRITORY = 'NT'
    AUSTRALIAN_CAPITAL_TERRITORY = 'ACT'


class Suburb(db.Model):
    __tablename__ = 'suburbs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    state = Column(SQLEnum(States), nullable=False)
    associatedPostCodes = relationship("PostCode", secondary=postcode_suburb_association,
                                       back_populates="associatedSuburbs")

    def __str__(self):
        return f"Suburb: {self.name}, State: {self.state.value}"


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)  # avoid using sensitive info as JWT are not encrypted
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(70), unique=True)

    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}"


# This table is ignored for migrations via the include_object hook to exclude this table
class Reporting(db.Model):
    __tablename__ = 'property_reporting'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(10))
    date_sold = db.Column(db.Date)
    avg_price = db.Column(db.Integer)

    def __str__(self):
        return f"state: {self.state}, date_sold: {self.date_sold}, avg_price:{self.avg_price}"

    def save(self, *args, **kwargs):
        raise NotImplementedError("This table is read-only.")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("This table is read-only.")
