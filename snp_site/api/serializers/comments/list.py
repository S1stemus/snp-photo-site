from rest_framework import serializers
from models_app.models import Comment
from api.views import comment



class CommentListSerializer(serializers.ModelSerializer):
    comments=serializers.SerializerMethodField()
    
    def get_comments(self, obj)->list:
        comments = obj.model_relation.all()
        return comment.CommentSerializer(comments, many=True).data
    
    class Meta:
        model = Comment
        fields = ['id','comment','user','content_type','object_id','comments']
        
