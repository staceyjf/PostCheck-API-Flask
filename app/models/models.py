from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from enum import Enum

# join table for the many-to-many relationship
postcode_suburb_association = Table('postcode_suburb', db.metadata,
    Column('postcode_id', Integer, ForeignKey('postcodes.id')),
    Column('suburb_id', Integer, ForeignKey('suburbs.id'))
)

class PostCode(db.Model):
    __tablename__ = 'postcodes'
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.String(4), nullable=False)
    # Define the M:M relationship via the join table, Postcode owns the relationship (not a bi-direction so only need to update one way)
    associatedSuburbs = relationship("Suburb", secondary=postcode_suburb_association)
    
class State(Enum):
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
    name = db.Column(db.String(100), nullable=False)
    state = Column(SQLEnum(State), nullable=False)