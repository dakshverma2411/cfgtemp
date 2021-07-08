from flask_restful import Resource, reqparse 
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.User import UserModel 
from models.Post import PostModel

USER_NOT_FOUND = 'User not found'
USER_ALREADY_EXISTS = "User already registered"
EMAIL_ALREADY_EXISTS = "Email ID already registered"
INTERNAL_SERVER_ERROR  = "Internal server error"
USER_DELETED = "User deleted successfully"

class User(Resource): # GET POST DELETE

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type = str,
        required = True
    )
    parser.add_argument(
        'password',
        type = str,
        required = True
    )

    #GET a user
    @jwt_required()
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json(), 200 
        else:
            return {'message':USER_NOT_FOUND}, 200

    #POST a new user
    def post(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return {'message':USER_ALREADY_EXISTS}, 400
        data = User.parser.parse_args()
        email = data['email']
        password = data['password']
        user = UserModel.find_by_email(email)
        if user:
            return {'message':EMAIL_ALREADY_EXISTS}, 400
        
        user = UserModel(username, email, password, [])
        try:
            user.save_to_db()

        except:
            return {'message':INTERNAL_SERVER_ERROR}, 500
        return user.json()

    #DELETE user
    @jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            try:
                user.delete_from_db()
                PostModel.objects(author = user.username).delete()
            except:
                return {'internal server error'}, 500 
            return {'message': USER_DELETED}, 200
        return {'message': USER_NOT_FOUND}, 404


class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type = str,
        required = True
    )
    parser.add_argument(
        'password',
        type = str,
        required = True
    )
    def post(self):
        data = UserLogin.parser.parse_args()
        username = data['username']
        password = data['password']
        user = UserModel.find_by_username(username)
        if user and user.password == password:
            access_token = create_access_token(identity = str(user.id), fresh = True)
            refresh_token = create_refresh_token(str(user.id))
            return {'access_token':access_token, 'refresh_token':refresh_token}, 200
        return {'message':"Invalid credentials"}, 401

class RefreshToken(Resource):

    @jwt_required(refresh = True)
    def post(self):
        user = get_jwt_identity()
        if user:
            new_token = create_access_token(identity = user, fresh = False)
            return {'access_token':new_token}, 200

class UserList(Resource):
    
    @jwt_required()
    def get(self):
        return {'users':[u.json() for u in UserModel.objects.all()]}

