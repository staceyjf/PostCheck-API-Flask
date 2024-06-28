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
    postcode = db.Column(db.String(4), nullable=False, unique=True)
    # Define the M:M relationship via the join table with a bi-directional relationship (back_populates))
    associatedSuburbs = relationship("Suburb", secondary=postcode_suburb_association, back_populates="associatedPostCodes")
    
    def __str__(self):
        # TASK: think about how to get suburbs properly
        return f"PostCode: {self.postcode}, associatedSuburbs: {self.associatedSuburbs}"
    
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
    name = db.Column(db.String(100), nullable=False, unique=True)
    state = Column(SQLEnum(State), nullable=False)
    associatedPostCodes = relationship("PostCode", secondary=postcode_suburb_association, back_populates="associatedSuburbs") 

    def __str__(self):
        return f"Suburb: {self.name}, State: {self.state.value}"
      
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True) # avoid using sensitive info as JWT are not encrypted 
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(70), unique = True)