from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from api.serializers.likes.show import LikeShowSerializer
from drf_spectacular.utils import extend_schema
from api.services.like.create import CreateLikeService
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from api.serializers.likes.post import LikePostSerializer


from rest_framework import status

class LikePostView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Лайки'],
        summary='создает лайк',
        description='создает лайк',
        request=LikePostSerializer,
        responses={
            200: LikeShowSerializer
        },
    )
    def post(self, request, *args, **kwargs):
        outcome=ServiceOutcome(CreateLikeService,{'current_user':request.user}|request.data )
        return Response(LikeShowSerializer(outcome.result).data, status=status.HTTP_200_OK)

