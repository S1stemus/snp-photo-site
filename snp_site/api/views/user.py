from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from rest_framework.views import APIView
from api.serializers.user.show import UserSerializer
from drf_spectacular.utils import extend_schema
from api.services.user.show import *
from api.services.user.user_photo import UserPhotoService
from api.serializers.photos.show import PhotoShowSerializer
from api.serializers.photos.list import PhotoListSerializer
from api.services.user.update import UserUpdateService
from api.services.user.create import CreateUserService
from api.serializers.user.register import UserRegisterSerializer
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from utils.pagination.custom_pagination import CustomPagination
from models_app.models.photo.fsm import State



class UserShowView(APIView):

    @extend_schema(
        tags=['Пользователи'],
        summary='Возвращает пользователя по id',
        description='Возвращает пользователя по id',
        responses={200: UserSerializer}
    )
    def get(self, request, *args, **kwargs):
        outcome=ServiceOutcome(UserShowService,{'user_id':kwargs['id']},{'current_user':request.user} )
        return Response(UserSerializer(outcome.result).data)
    @extend_schema(
        tags=['Пользователи'],
        summary='Обновляет пользователя по id',
        description='Обновляет пользователя по id',
        responses = {200: UserSerializer},
        request = UserSerializer
    )
    def put(self, request, *args, **kwargs):
        outcome=ServiceOutcome(UserUpdateService,{'user_id':kwargs['id'],'current_user':request.user} |request.data.dict(),request.FILES)
        return Response(UserSerializer(outcome.result).data)

class ListUserPhotoView(APIView):
    @classmethod
    def _fetch_query_params_dict(cls, request) -> dict:
        return {
            key: value if len(value) > 1 else value[0]
            for key, value in dict(request.query_params).items()
        }

    @extend_schema(
        tags=['Пользователи'],
        summary='Возвращает все фото пользователя',
        description='Возвращает все фото пользователя',
        responses={200: PhotoListSerializer},
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
             OpenApiParameter(
                name='sort_field',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                enum=UserPhotoService.SortFields.values,
                description='Поле сортировки',
                default='created_at'
            ),
            OpenApiParameter(
                name='sort_direction',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                enum=('asc','desc'),
                description='Направление сортировки',
                default='desc'
                
            ),
            OpenApiParameter(
                name='state',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Фильтрация по статусу',
                enum=State.values,
                many=True,
                default='approved'               
            ),           
        ]
    )
    def get(self, request, *args, **kwargs):       
        data=self._fetch_query_params_dict(request)
        user=None if request.user.is_anonymous else request.user
        print(data)
        outcome=ServiceOutcome(UserPhotoService,{'user_id':kwargs['id'],'current_user':user}|data,request.FILES)
        return Response(
            {
            "pagination": CustomPagination(
                outcome.result,
                current_page=outcome.service.cleaned_data["page"],
                per_page=outcome.service.cleaned_data["per_page"],
            ).to_json(),
            "results": PhotoListSerializer(
                outcome.result.object_list, many=True
            ).data,
            },
            status=status.HTTP_200_OK,
            )
       
        
    

class RegisterUserView(APIView):
    @extend_schema(
        tags=['Пользователи'],
        summary='Создает пользователя ',
        description='Создает пользователя',
        responses = {200: UserSerializer},
        request = UserRegisterSerializer
    )
    def post(self, request, *args, **kwargs):
        outcome=ServiceOutcome(CreateUserService(),request.data.dict(),request.FILES)
        return outcome.result