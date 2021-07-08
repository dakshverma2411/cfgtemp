import mongoengine as me 
import datetime

class PostModel(me.Document):
    author = me.StringField()
    date = me.DateTimeField(default = datetime.datetime.now)
    content = me.StringField(required = True)
    likes = me.ListField(me.StringField())
    comments = me.ListField(me.ReferenceField('CommentModel', reverse_delete_rule = me.CASCADE))

    def json(self):
        return {'id':str(self.id), 'author':self.author, 'date':str(self.date), 'content':self.content, 'likes':self.likes, 'comments':[{'by':c.commentor, 'comment':c.comment} for c in self.comments]}

    def __init__(self, author, content, *args, **kwargs):
        super(me.Document, self).__init__(*args, **kwargs)
        self.author = author 
        self.content = content 

    def add_like(self, like):
        self.likes.append(like)
        self.save()

    def delete_like(self, like):
        PostModel.objects(id = self.id).update(pull__likes=like)
        self.save()
    
    @classmethod
    def find_by_id(self, _id):
        return PostModel.objects(id = _id).first()
    
    def save_to_db(self):
        self.save()
    
    def delete_from_db(self):
        self.delete()
