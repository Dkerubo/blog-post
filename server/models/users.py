from database import db 
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    
    #tablename
    __tablename__ = 'users'
    
    #primary key
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    
    #relationship 
    post = db.relationship('Post', back_populates='user')