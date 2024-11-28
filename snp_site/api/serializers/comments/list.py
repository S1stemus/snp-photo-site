from rest_framework import serializers
from models_app.models import Comment
from api.views import comment
from api.serializers.user.show import UserSerializer


class CommentListSerializer(serializers.ModelSerializer):
    comments=serializers.SerializerMethodField()
    user=UserSerializer()
    
    def get_comments(self, obj)->list:
        comments = obj.model_relation.all()
        return comment.CommentListSerializer(comments, many=True).data
    
    class Meta:
        model = Comment
        fields = ['id','comment','user','content_type','object_id','comments']
        
