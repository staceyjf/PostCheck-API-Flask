from flask_sqlalchemy import SQLAlchemy #ORM
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

# database set up
db = SQLAlchemy(metadata=metadata)

class Todo(db.Model):
    __tablename__ = 'todo' 
    id = db.Column(db.Integer, primary_key=True)
    dueDate = db.Column(db.Date, nullable=False)  
    title = db.Column(db.String(120), nullable=False)
    task = db.Column(db.String(500), nullable=False)
    isComplete = db.Column(db.Boolean, default=False)  
    colour_id = db.Column(db.Integer, db.ForeignKey('colour.id'), nullable=False) #setting up the M:1 relationship
    colour = db.relationship('Colour', back_populates='todos') #ensures a bidirectional relationship  

class Colour(db.Model):
    __tablename__ = 'colour'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    hexCode = db.Column(db.String(10), unique=True, nullable=False)
    todos = db.relationship('Todo', back_populates='colour') #setting up the 1:M relationship