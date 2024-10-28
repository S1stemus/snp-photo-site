from rest_framework import serializers
from models_app.models import Photo
class PhotoSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ['id','photo', 'caption', 'user', 'created_at', 'updated_at','state','like_count','comment_count']
    def get_like_count(self, obj):
        return obj.likes.count()
    def get_comment_count(self, obj):
        return obj.model_relation.count()