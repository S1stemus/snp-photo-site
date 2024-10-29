from django.http import Http404
from django.test import tag
from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from api.serializers.comments.update import CommentUpdateSerializer
from api.serializers.comments.show import CommentShowSerializer
from api.serializers.comments.list import CommentListSerializer
from api.services.comment.show import RetrieveCommentsByIdService
from drf_spectacular.utils import extend_schema
from api.services.comment.delete import DeleteCommentService
from api.serializers.comments.create import CommentCreateSerializer
from api.services.comment.update import UpdateCommentService
from api.services.comment.create import CreateCommentService
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class PostCommentView(APIView):

    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=['Комментарии'],
        summary='создает комментарии',
        description='создает комментарии',
        request=CommentCreateSerializer,
        responses={200: CommentShowSerializer}
    )
    def post(self, request, *args, **kwargs):
        outcome=ServiceOutcome(CreateCommentService,request.data | {'current_user':request.user} )
        return Response(CommentShowSerializer(outcome.result).data, status=status.HTTP_201_CREATED)       



class RetreiveCommentView(APIView):
    

    @extend_schema(
        tags=['Комментарии'],
        summary='Возвращает комментарии по id',
        description='Возвращает комментарии по id',
        responses={
            200: CommentListSerializer
        }
    )
    def get(self, request,*args, **kwargs):
        outcome=ServiceOutcome(RetrieveCommentsByIdService,{'id':kwargs['id']} )
        return Response(CommentShowSerializer(outcome.result,many=True).data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Комментарии'],
        summary='удаляет комментарии по id',
        description='удаляет комментарии по id',
        responses={
            200: None
        }
    )
    def delete(self, request, *args, **kwargs):
        outcome=ServiceOutcome(DeleteCommentService,{'id':kwargs['id']} )
        return Response(None, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Комментарии'],
        summary='обновляет комментарии по id',
        description='обновляет комментарии по id',
        responses={
            200: CommentShowSerializer
        },
        request=CommentUpdateSerializer
    )
    def put(self, request, *args, **kwargs):
        outcome=ServiceOutcome(UpdateCommentService,{'id':kwargs['id']} | request.data, request.FILES, )
        return Response(CommentUpdateSerializer(outcome.result).data, status=status.HTTP_200_OK)
    
