import mongoengine as me
# from models.Post import PostModel
# from models.User import UserModel
import datetime

class CommentModel(me.Document):
    post = me.StringField()
    comment = me.StringField()
    comment_date = me.DateTimeField(default = datetime.datetime.now)
    commentor = me.StringField()

    def __init__(self, post, comment, commentor, *args, **kwargs):
        super(me.Document, self).__init__(*args, **kwargs)
        self.post = post
        self.comment = comment
        self.commentor = commentor

    # @classmethod 
    # def find_all_posts_commented_by(cls, commentor):
    #     return UserModel.objects(commentor = commentor).all() 
    
    def save_to_db(self):
        self.save()

    def delete_from_db(self):
        self.delete()