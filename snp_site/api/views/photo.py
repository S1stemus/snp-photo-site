from tkinter.filedialog import Open
from requests import delete
from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from api.serializers.photos.photo_serializer import PhotoSerializer
from api.serializers.photos.photo_post_serializer import PhotoPostSerializer
from api.services.photo.show import ShowPhotoService
from models_app.models.photo.models import Photo
from drf_spectacular.utils import extend_schema
from api.services.photo.delete import DeletePhotoService
from api.services.photo.update import UpdatePhotoService
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from api.services.photo.list import ListPhotoService
from api.services.photo.create import CreatePhotoService
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from utils.pagination.custom_pagination import CustomPagination
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes



class ListCreatePhotoView(APIView):

    

    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=['Фотографии'],
        summary='Создает фотографию',
        description='Создает фотографию',
        request=PhotoPostSerializer,
        responses={
            200: PhotoSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        outcome=ServiceOutcome(CreatePhotoService, {'current_user':request.user}, request.FILES)
        return Response(PhotoSerializer(outcome.result).data)
    
    
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Фотографии'],
        summary='Возвращает все фотографии',
        description='Возвращает все фотографии',
        responses={
            200: PhotoSerializer
        },
        parameters=[
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Номер страницы',
                default=1
            ),
            OpenApiParameter(
                name='per_page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Количество элементов на странице',
                default=10
            ),
            
        ]
        
    )
    def get(self, request, *args, **kwargs):

        outcome=ServiceOutcome(ListPhotoService,request.query_params.dict())
        print(outcome.result)
        return Response(
        {
            "pagination": CustomPagination(
                outcome.result,
                current_page=outcome.service.cleaned_data["page"],
                per_page=outcome.service.cleaned_data["per_page"],
            ).to_json(),
            "results": PhotoSerializer(
                outcome.result.object_list, many=True
            ).data,
        },
    status=status.HTTP_200_OK,
)


class RetreivePhotoView(APIView):
    permission_classes = [AllowAny]
     
    @extend_schema(
        tags=['Фотографии'],
        summary='Возвращает фотографию по id',
        description='Возвращает фотографию по id',
        responses={
            200: PhotoSerializer
        }
       
    )    
    def get(self, request, *args, **kwargs):
        outcome=ServiceOutcome(ShowPhotoService,{'id':kwargs['id']} )
        return Response(PhotoSerializer(outcome.result).data)
    
   
    
    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=['Фотографии'],
        summary='Удаляет фотографию по id',
        description='Удаляет фотографию по id',
        responses={
            200: PhotoSerializer
        }
    )    
    def delete(self, request, *args, **kwargs):
        outcome=ServiceOutcome(DeletePhotoService,{'id':kwargs['id']} )
        if outcome.result:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        tags=['Фотографии'],
        summary='Обновляет фотографию по id',
        description='Обновляет фотографию по id',
        responses={
            200: PhotoSerializer
        },
        request=PhotoPostSerializer
    )    
    def put(self, request, *args, **kwargs):
        outcome=ServiceOutcome(UpdatePhotoService,{'id':kwargs['id'],'current_user':request.user} | request.data, request.FILES,)
        return Response(PhotoSerializer(outcome.result).data)
    
   
    

    


