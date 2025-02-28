from flask import Flask, jsonify, make_response 
from models import Category, User, Post
from flask_migrate import Migrate
from database import db 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

migrate = Migrate(app, db)

db.init_app(app)


# Get users 
@app.route('/users')
def users():
    users = []
    
    for i in User.query.all():
        users.append(i.to_dict())
    
    response_body = jsonify(users)
    status_code = 200
    
    return make_response(response_body, status_code)



if __name__ == '__main__':
    app.run(port=5555, debug=True)



