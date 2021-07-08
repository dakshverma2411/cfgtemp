from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.Post import PostModel 
from models.User import UserModel
# from models.Likes import LikeModel
import datetime

POST_NOT_FOUND = "Post not found"
POST_DELETED = "Post deleted successfully"
INTERNAL_SERVER_ERROR = "Internal server error"
USER_NOT_FOUND = 'User not found'

class Post(Resource): #GET, PUT, DELETE

    parser = reqparse.RequestParser()
    parser.add_argument(
        'author',
        type = str,
        required = True
    )
    parser.add_argument(
        'content',
        type = str,
        required = True
    )
    #GET post by id
    @jwt_required()
    def get(self, id):
        post = PostModel.find_by_id(id)
        if post:
            return post.json(), 200
        return {'message':POST_NOT_FOUND}, 404

    #PUT
    @jwt_required()
    def put(self, id):
        post = PostModel.find_by_id(id)
        if post:
            data = Post.parser.parse_args()
            author_username = data['author']
            content = data['content']
            author = UserModel.find_by_username(author_username)
            post.author = author_username
            post.content = content 
            post.date = datetime.datetime.now

            try:
                post.save_to_db()
            except:
                return {'message':INTERNAL_SERVER_ERROR}, 500
            return post.json()
        return {'message':POST_NOT_FOUND}

    #DELETE
    @jwt_required()
    def delete(self, id):
        post = PostModel.find_by_id(id)
        if post:
            try:
                username = post.author
                user = UserModel.find_by_username(username)
                if user:
                    user.delete_post(post)
                    post.delete_from_db()
            except Exception as e:
                return {'message':INTERNAL_SERVER_ERROR}, 500
            return {'message':POST_DELETED}, 200
        return {'message':POST_NOT_FOUND}, 404


class PostAdd(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'author',
        type = str,
        required = True
    )
    parser.add_argument(
        'content',
        type = str,
        required = True
    )


    @jwt_required()
    def post(self):
        data = PostAdd.parser.parse_args()
        author_username = data['author']
        content = data['content']
        author = UserModel.find_by_username(author_username)
        if author:
            post = PostModel(author_username, content)
            try:
                post.save_to_db()
                author.add_post(post)
            except Exception as e:
                return {'message':INTERNAL_SERVER_ERROR + str(e)}, 500
            return post.json()
        return {'message':USER_NOT_FOUND}


class PostList(Resource): #GET

    @jwt_required()
    def get(self):
        return {'posts':[p.json() for p in PostModel.objects.all()]} 