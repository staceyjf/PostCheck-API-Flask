from app.extensions import db

class Colour(db.Model):
    __tablename__ = 'colour'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    hexCode = db.Column(db.String(6), unique=True, nullable=False) #hexcodes are 3/6 chars
    todos = db.relationship('Todo', back_populates='colour') #setting up the 1:M relationship
    
    # more reader friendly representation of the todo instance
    def __repr__(self):
        return f"<Colour id={self.id}, name='{self.name}', hexCode={self.hexCode}, todos={self.todos}>"