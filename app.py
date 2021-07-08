from flask import Flask 
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Api 
from flask_jwt_extended import JWTManager
from resources.Comments import *
from resources.Post import Post, PostList, PostAdd
from resources.User import User, UserList, UserLogin, RefreshToken
from resources.Likes import *
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost/social_media'
}

app.secret_key = 'some_secret_key'

api = Api(app)
jwt = JWTManager(app)

# adding resource
api.add_resource(User, '/user/<string:username>') # GET, POST, DELETE
api.add_resource(UserLogin, '/login') # POST
api.add_resource(RefreshToken, '/refresh') # POST
api.add_resource(UserList,'/users') #GET with pagination
api.add_resource(PostList, '/posts') # GET with pagination
api.add_resource(Post, '/post/<string:id>') #GET, DELETE, PUT
api.add_resource(PostAdd, '/post') # POST a post
api.add_resource(Like, '/post/likes') #POST and DELETE
# api.add_resource(Comment, '/post/comments/<string:id>') #POST, PUT and DELETE


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug = True)