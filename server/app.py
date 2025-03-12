from flask import Flask, jsonify, make_response, request, session
from models import Category, User, Post
from flask_migrate import Migrate
from database import db 
from flask_restful import Resource, Api
import os 
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

migrate = Migrate(app, db)

db.init_app(app)

#create an api instance/object
api = Api(app)

#create a secret key 
secret_key = os.urandom(23)
app.secret_key = secret_key


'''
POST /auth/register
'''
class Register(Resource):
    def post(self):
        
        data = request.get_json()
        
        full_name = data['full_name']
        email = data['email']
        password = data['password']
        
        user = User.query.filter(User.email == email).first()
        
        if user:
            response = make_response(
                jsonify({
                    'message': 'user already exist!'
                }), 
                409
            )
            response.headers['Content-Type'] = 'application/json'
            return response
        
        #hash the password before we store it 
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        new_user = User(
            full_name = full_name,
            email = email,
            password = hashed_password.decode('utf8')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        #session['user_id'] = new_user.id
        
        response = make_response(
            jsonify({
                'message': 'Registration success!!'
            }),
            201
        )
        response.headers['Content-Type'] = 'application/json'
        return response
api.add_resource(Register, '/auth/register')

'''
POST /auth/login
'''
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        email = data['email']
        password = data['password']
        
        user = User.query.filter(User.email == email).first()
        
        if user is None:
            response = make_response(
                jsonify({
                    "Error": 'Unauthorized Access'
                }), 
                401
            )
            response.headers['Content-type'] = 'application/json'
            return response
        
        #check the password 
        hashed_password = user.password
        
        if bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')):
            
            session['user_id'] = user.id
            
            response = make_response(
                jsonify({
                    'message': 'login success'
                }), 
                200
            )
            return response
        else:
            response = make_response(
                jsonify({
                    'message': 'password incorrect!'
                }),
                403
            )
            return response
api.add_resource(Login, '/auth/login')
        
'''
GET /posts
'''       
class Posts(Resource):
    def get(self):
        #get the user id from the session
        user_id = session.get('user_id')
        
        #check if the the user_id exists 
        if user_id is None:
            response = make_response(
                jsonify({
                    'message': 'Unauthorized access'
                }), 
                401
            )
            return response
        
        posts = []
        
        for post in Post.query.filter(Post.user_id == user_id).all():
            posts.append(post.to_dict())
        
        if len(posts) == 0:
            response = make_response(
                jsonify({
                    'message': 'No posts Found'
                }),
                200
            )
            return response
        
        response = make_response(
            jsonify(posts), 
            200
        )
        return response
    
api.add_resource(Posts, '/posts') 
        



if __name__ == '__main__':
    app.run(port=5555, debug=True)