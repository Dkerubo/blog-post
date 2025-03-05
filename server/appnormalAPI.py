from flask import Flask, jsonify, make_response, request
from models import Category, User, Post
from flask_migrate import Migrate
from database import db 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

migrate = Migrate(app, db)

db.init_app(app)

'''
1. GET /users
2. POST /users
'''
@app.route('/users', methods = ['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = []
        
        for i in User.query.all():
            users.append(i.to_dict())
            response_body = jsonify(users)
            status_code =200
            return make_response(response_body, status_code)
    elif request.method == 'post':
        
        new_user = User (
            full_name = request.form.get('full_name'),
            email = request.form.get('email')     
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        response_body = {
            'message' : 'user created successfully'   
        }
        status_code = 201

'''
GET /users/id
PUT/PATCH /users/id
DELETE /users/id
'''
@app.route('/users/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def user(id):
    user=User.query.filter(User.id == id).first()
    if user is None:
            response_body = {
                'Error':'User does not exist!'
            }    
            status_code = 404
            return make_response(response_body, status_code)                
    else :
        if request.method == 'GET':
            response_body = jsonify(user.to_dict()) 
            status_code = 200
            return make_response(response_body, status_code)
        elif request.method == 'Put':
            for att in request.form:
                setattr(user, attr, request.form.get(attr))
                db.session.add(user)
                db.session.commit()
                response_body = jsonify(user.to_dict())  
                status_code =200 
                return make_response(response_body, status_code)
        elif request.method == 'DELETE':
            
            db.session.delete(user)
            db.session.commit()
            
            response_body = {
                'message': 'user deleted successfully!'
            }
            status_code = 200
            
            return make_response(response_body, status_code)
            
# # Get users 
# @app.route('/users')
# def users():
#     users = []
    
#     for i in User.query.all():
#         users.append(i.to_dict())
    
#     response_body = jsonify(users)
#     status_code = 200
    
#     return make_response(response_body, status_code)



if __name__ == '__main__':
    app.run(port=5555, debug=True)



