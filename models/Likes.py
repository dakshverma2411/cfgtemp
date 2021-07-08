# import mongoengine as me
# # from models.Post import PostModel
# # from models.User import UserModel
# from mongoengine.queryset.visitor import Q

# class LikeModel(me.Document):
#     post = me.ReferenceField(UserModel, reverse_delete_rule = me.NULLIFY)
#     likedby = me.ReferenceField(PostModel, reverse_delete_rule = me.NULLIFY)

#     def __init__(self, post, likedby, *args, **kwargs):
#         super(me.Document, self).__init__(*args, **kwargs)
#         self.post = post
#         self.likedby = likedby

#     @classmethod 
#     def find_by_post_and_user(cls, likedby, post):
#         return LikedModel.objects(Q(likedby = likedby) | Q(post = post)).first() 
    
#     def save_to_db(self):
#         self.save()

#     def delete_from_db(self):
#         self.delete()