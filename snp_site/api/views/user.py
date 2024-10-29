from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from rest_framework.views import APIView
from api.serializers.user.user_serializer import UserSerializer
from drf_spectacular.utils import extend_schema
from api.services.user.show import *
from api.services.user.user_photo import UserPhotoService
from api.serializers.photos.photo_serializer import PhotoSerializer

class UserShowView(APIView):

    @extend_schema(
        tags=['Пользователи'],
        summary='Возвращает пользователя по id',
        description='Возвращает пользователя по id',
        responses={200: UserSerializer}
    )
    def get(self, request, *args, **kwargs):
        outcome=ServiceOutcome(UserShowService,{'user_id':kwargs['id']},{'current_user':request.user} )
        print(outcome.result)
        return Response(UserSerializer(outcome.result).data)
class ListUserPhotoView(APIView):

    @extend_schema(
        tags=['Пользователи'],
        summary='Возвращает все фото пользователя',
        description='Возвращает все фото пользователя',
        responses={200: PhotoSerializer}
    )
    def get(self, request, *args, **kwargs):
        breakpoint()
        outcome=ServiceOutcome(UserPhotoService,{'user_id':kwargs['id']},{'current_user':request.user})
        print(outcome.result)
        return Response(PhotoSerializer(outcome.result,many=True).data)