from rest_framework import serializers
from models_app.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        ref_name='api_comment_serializer'