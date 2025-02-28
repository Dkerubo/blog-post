from app import app
from models import Category, User, Post
from faker import Faker
from database import db
import random

fake = Faker()

with app.app_context():
    
    print('Seeding the Database!')
    
    users = []
    
    for i in range(5):
        users.append(User(
            full_name = fake.name(),
            email = fake.email()
        ))
        
    db.session.add_all(users)
    
    posts = []
    
    for i in range(10):
        posts.append(Post(
            title = fake.word(),
            description = fake.word(),
            user_id = random.randint(1,5),
            category_id = random.randint(1,3)
        ))
        
    db.session.add_all(posts)
    
    categories = []
    
    for i in range(4):
        categories.append(Category(
            name = fake.company(),
        ))
        
    db.session.add_all(categories)
    
    db.session.commit()
    
    print('Seeding complete!!')
    
    