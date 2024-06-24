from app.extensions import db
from datetime import datetime

class Todo(db.Model):
    __tablename__ = 'todo' 
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.Date, nullable=False, default=datetime.now) 
    dueDate = db.Column(db.Date, nullable=False)  
    title = db.Column(db.String(120), nullable=False)
    task = db.Column(db.String(500), nullable=False)
    isComplete = db.Column(db.Boolean, default=False)  
    colour_id = db.Column(db.Integer, db.ForeignKey('colour.id'), nullable=False) #setting up the M:1 relationship
    colour = db.relationship('Colour', back_populates='todos') #ensures a bidirectional relationship
    
    # more reader friendly representation of the todo instance
    def __repr__(self):
        return f"<Todo id={self.id}, title='{self.title}', dueDate={self.dueDate}, isComplete={self.isComplete}>"