from rest_framework import serializers
from models_app.models import Photo
from api.serializers.user.show import UserSerializer
class PhotoShowSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    user=UserSerializer()
 
    class Meta:
        model = Photo
        fields = ['id','photo','name', 'description', 'user', 'created_at', 'updated_at','state','like_count','comment_count']