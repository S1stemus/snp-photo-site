from rest_framework import serializers
from models_app.models import Comment
from api.views import comment
from api.serializers.user.show import UserSerializer


class CommentShowSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    
    class Meta:
        model = Comment
        fields = ['id','comment','user','content_type','object_id','created_at','updated_at']
        