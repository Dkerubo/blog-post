from database import db 
from sqlalchemy_serializer import SerializerMixin


class Category(db.Model, SerializerMixin):
    
    #tablename
    __tablename__ = 'categories'
    
    serialize_rules = ('-post',)
    
    #primary key
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)

    
    #relationship 
    post = db.relationship('Post', back_populates='category')