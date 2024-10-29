from rest_framework import serializers
from models_app.models import Comment
from api.views import comment


class CommentShowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id','comment','user','content_type','object_id','created_at','updated_at']
        