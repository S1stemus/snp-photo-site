from api.serializers.photos.create import PhotoCreateSerializer
from api.serializers.photos.list import PhotoListSerializer
from api.serializers.photos.show import PhotoShowSerializer
from api.serializers.photos.update import PhotoUpdateSerializer
from api.services.photo.create import CreatePhotoService
from api.services.photo.delete import DeletePhotoService
from api.services.photo.list import ListPhotoService
from api.services.photo.show import ShowPhotoService
from api.services.photo.update import UpdatePhotoService
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from utils.pagination.custom_pagination import CustomPagination


class ListCreatePhotoView(APIView):
    @classmethod
    def _fetch_query_params_dict(cls, request) -> dict:
        return {
            key: value if len(value) > 1 else value[0]
            for key, value in dict(request.query_params).items()
        }

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Фотографии"],
        summary="Создает фотографию",
        description="Создает фотографию",
        request=PhotoCreateSerializer,
        responses={200: PhotoShowSerializer},
    )
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CreatePhotoService,
            {"current_user": request.user} | request.data.dict(),
            request.FILES,
        )
        return Response(PhotoShowSerializer(outcome.result).data)

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Фотографии"],
        summary="Возвращает все фотографии",
        description="Возвращает все фотографии",
        responses={200: PhotoListSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="search_field",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Поиск по строке",
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Номер страницы",
                default=1,
            ),
            OpenApiParameter(
                name="per_page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Количество элементов на странице",
                default=10,
            ),
            OpenApiParameter(
                name="sort_field",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=ListPhotoService.SortFields.values,
                required=False,
                description="Поле сортировки",
                default="created_at",
            ),
            OpenApiParameter(
                name="sort_direction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                enum=("asc", "desc"),
                description="Направление сортировки",
                default="desc",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        data = self._fetch_query_params_dict(request)

        outcome = ServiceOutcome(ListPhotoService, data)
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


class RetreivePhotoView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Фотографии"],
        summary="Возвращает фотографию по id",
        description="Возвращает фотографию по id",
        responses={200: PhotoShowSerializer},
    )
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ShowPhotoService, {"id": kwargs["id"]})
        return Response(PhotoShowSerializer(outcome.result).data)


class UpdateDeletePhotoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Фотографии"],
        summary="Удаляет фотографию по id",
        description="Удаляет фотографию по id",
        responses={200: None},
    )
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DeletePhotoService, {"id": kwargs["id"],"current_user":request.user})
        if outcome.result:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=["Фотографии"],
        summary="Обновляет фотографию по id",
        description="Обновляет фотографию по id",
        responses={200: PhotoShowSerializer},
        request=PhotoUpdateSerializer,
    )
    def put(self, request, *args, **kwargs):
        self.permission_classes = [
            IsAuthenticated
        ]  # Устанавливаем разрешения для этого метода
        self.check_permissions(request)  # Проверяем разрешения
        outcome = ServiceOutcome(
            UpdatePhotoService,
            {"id": kwargs["id"], "current_user": request.user} | request.data.dict(),
            request.FILES,
        )
        return Response(PhotoShowSerializer(outcome.result).data)
