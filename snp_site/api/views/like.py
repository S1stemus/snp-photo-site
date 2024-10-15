from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from api.serializers.like_serializer import LikeSerializer
from drf_spectacular.utils import extend_schema
from api.services.like.create import CreateLikeService
from rest_framework.permissions import IsAuthenticated
from api.serializers.like_post_serializer import LikePostSerializer

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
            tags=['Лайки'], 
            summary='Добавление лайка', 
            description='Добавление лайка', 
            request= LikePostSerializer,
            responses={200: LikeSerializer}

            )
    def post(self, request, *args, **kwargs):
        outcome=ServiceOutcome(CreateLikeService,{'user':request.user.id,'photo':kwargs['photo_id']} )
        return Response(LikeSerializer(outcome.result).data)

