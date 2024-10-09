from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from api.serializers.photo_serializer import PhotoSerializer
from api.services.photo.show import ShowPhotoService
from models_app.models.photo.models import Photo
from drf_spectacular.utils import extend_schema


class RetreivePhotoView(APIView):

    @extend_schema(
        tags=['Фотографии'],
        summary='Возвращает фотографию по id',
        description='Возвращает фотографию по id',
        responses={
            200: PhotoSerializer
        },
        request=PhotoSerializer
    )
    def get(self, request, *args, **kwargs):
        outcome=ServiceOutcome(ShowPhotoService,{'id':kwargs['id']} )
        return Response(PhotoSerializer(outcome.result).data)
    
    # def delete()


