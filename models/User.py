import mongoengine as me

class UserModel(me.Document):
    username = me.StringField(required = True, unique = True)
    email = me.StringField(required = True, unique = True)
    password = me.StringField(requried = True)
    posts = me.ListField(me.ReferenceField('PostModel', reverse_delete_rule = me.CASCADE))

    def __init__(self, username, email, password, posts, *args, **kwargs):
        super(me.Document, self).__init__(*args, **kwargs)
        self.username = username
        self.email = email
        self.password = password
        self.posts = posts

    def json(self):
        return {'username':self.username, 'email':self.email, 'posts':[p.json() for p in self.posts]}

    @classmethod 
    def find_by_email(cls, email):
        return UserModel.objects(email = email).first() 
    
    @classmethod
    def find_by_username(cls, username):
        return UserModel.objects(username = username).first()
    
    @classmethod 
    def find_by_id(cls, id):
        return UserModel.objects(id = id).first()

    def add_post(self, post):
        self.posts.append(post)
        self.save()

    def delete_post(self, post):
        UserModel.objects(username = self.username).update(pull__posts = post)
        self.save()
    
    def save_to_db(self):
        self.save()

    def delete_from_db(self):
        self.delete()