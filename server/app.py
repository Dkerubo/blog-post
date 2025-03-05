from flask import Flask, jsonify, make_response, request 
from models import Category, User, Post
from flask_migrate import Migrate
from database import db 
from flask_restful import Resource, Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

migrate = Migrate(app, db)

db.init_app(app)

#create an api instance/object
api = Api(app)

'''
1.GET  /users 
2. POST /users 
'''
# define class for you resouce 
class Users(Resource): 
    #http method/verb
    def get(self):
        users = []
        
        for i in User.query.all():
            users.append(i.to_dict())
            
        response_body = jsonify(users)
        status_code = 200
        
        return make_response(response_body, status_code)
    
    def post(self):
        
        new_user = User(
            full_name = request.form.get('full_name'),
            email = request.form.get('email')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        response_body = {
            'message': 'user created!'
        }
        status_code = 201
        
        return make_response(response_body, status_code)
api.add_resource(Users, '/users')

'''
GET  /users/id
PUT/PATCH   /users/id
DELETE  /users/id
'''

class UserById(Resource):
    def get(self, id):
        
        user = User.query.filter(User.id == id).first()
        
        if user is None:
            response = {
                'message': 'User doe not exists'
            }
            status_code = 404
            
            return make_response(response, status_code)
        
        response = jsonify(user.to_dict())
        status_code = 200
        
        return make_response(response, status_code)
    
    def put(self, id):
        
        user = User.query.filter(User.id == id).first()
        
        if user is None:
            response = {
                'message': 'User doe not exists'
            }
            status_code = 404
            
            return make_response(response, status_code)
        
        for attr in request.form:
            setattr(user, attr, request.form.get(attr))
        
        db.session.add(user)
        db.session.commit()
        
        response = jsonify(user.to_dict())
        status_code = 200
        
        return make_response(response, status_code)
    
    def delete(self, id):
        # Error handling: Check if user exists
        user = User.query.filter_by(id=id).first()
        if user is None:
            response = {
                'message': 'User does not exist'
            }
            status_code = 404
            return make_response(response, status_code)

        # Delete user from DB
        db.session.delete(user)
        
        # Persist changes
        db.session.commit()

        # Send a response to the user
        response_body = {
            'message': 'User deleted successfully'
        }
        status_code = 200
        return make_response(response_body, status_code)

api.add_resource(UserById, '/users/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)


