from django.test import tag
from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from api.serializers.comment_serializer import CommentSerializer
from api.services.comment.show import RetrieveCommentsByIdService
from drf_spectacular.utils import extend_schema
from api.services.comment.create import CreateCommentService

class RetreiveCommentView(APIView):
    

    @extend_schema(
        tags=['Комментарии'],
        summary='Возвращает комментарии по id',
        description='Возвращает комментарии по id',
        responses={
            200: CommentSerializer
        }
    )
    def get(self, request,*args, **kwargs):
        outcome=ServiceOutcome(RetrieveCommentsByIdService,{'id':kwargs['id']} )
        return Response(CommentSerializer(outcome.result).data)
    def post(self, request, *args, **kwargs):
        outcome=ServiceOutcome(CreateCommentService,request.data | {'current_user':request.user} ) 
        