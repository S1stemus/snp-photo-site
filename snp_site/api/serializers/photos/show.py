from rest_framework import serializers
from models_app.models import Photo
from api.serializers.user.show import UserSerializer
class PhotoShowSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    user=UserSerializer()
    def get_like_count(self, obj)->int:
        return obj.likes.count()
    def get_comment_count(self, obj)->int:      
        return obj.model_relation.count()
    class Meta:
        model = Photo
        fields = ['id','photo','name', 'description', 'user', 'created_at', 'updated_at','state','like_count','comment_count']