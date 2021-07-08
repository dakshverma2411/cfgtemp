from flask_restful import Resource, reqparse 
from flask_jwt_extended import jwt_required
from models.Post import PostModel 
from models.User import UserModel


INTERNAL_SERVER_ERROR = "Internal Server error"
LIKED = "Post Liked"

class Like(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'post',
        type = str,
        required = True
    )

    parser.add_argument(
        'likedby',
        type = str,
        required = True
    )

    @jwt_required()
    def post(self):
        data = Like.parser.parse_args()
        post_id = data['post']
        username = data['likedby']
        user = UserModel.find_by_username(username)
        post = PostModel.find_by_id(post_id)
        if user and post:
            try:
                post.add_like(username)
            except Exception as e:
                return {'message':INTERNAL_SERVER_ERROR + str(e)}, 500
            return {'message':LIKED}, 200
        return {'message':'BAD REQUEST'}, 400

    @jwt_required()
    def delete(self):
        data = Like.parser.parse_args()
        post_id = data['post']
        username = data['likedby']
        user = UserModel.find_by_username(username)
        post = PostModel.find_by_id(post_id)

        if user and post:
            # like = LikeModel.find_by_post_and_user(user, post)
            try:
                # like.delete_from_db()
                post.delete_like(username)
            except Exception as e:
                return {'message':INTERNAL_SERVER_ERROR+str(e)}, 500
            return {'message':'Unliked'}, 200
        return {'message':'BAD REQUEST'}, 400