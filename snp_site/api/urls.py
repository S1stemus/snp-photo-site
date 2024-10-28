from api.views.photo import RetreivePhotoView
from api.views.comment import RetreiveCommentView
from django.urls import path
from api.views.comment import RetreiveCommentView
from api.views.like import LikePostView
from api.views.comment import PostCommentView
from api.views.photo import ListCreatePhotoView
from api.views.user import *


urlpatterns=[
    path('photo/<int:id>/', RetreivePhotoView.as_view()),
    path('comments/<int:id>/', RetreiveCommentView.as_view()),
    path('comments/', PostCommentView.as_view()),
    path('like/', LikePostView.as_view()),
    path('photos/', ListCreatePhotoView.as_view()),
    path('users/<int:id>/', UserShowView.as_view()),
    path('users/photos/<int:id>/', ListUserPhotoView.as_view()),
]
