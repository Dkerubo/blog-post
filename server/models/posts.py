from database import db 
from sqlalchemy_serializer import SerializerMixin


class Post(db.Model, SerializerMixin):
    
    #tablename
    __tablename__ = 'posts'
    
    serialize_rules = ('-user',)
    
    #primary key
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    
    #foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    #relationship 
    user = db.relationship('User', back_populates='post')
    category = db.relationship('Category', back_populates='post')