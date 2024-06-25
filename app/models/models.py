from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey, String

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

class Suburb(db.Model):
    __tablename__ = 'suburbs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)