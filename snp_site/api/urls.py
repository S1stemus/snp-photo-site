from api.views.comment import PostCommentView, RetreiveCommentView
from api.views.like import LikePostView
from api.views.photo import (
    ListCreatePhotoView,
    RetreivePhotoView,
    UpdateDeletePhotoView,
)
from api.views.user import ListUserPhotoView, RegisterUserView, UserShowView
from django.urls import path

urlpatterns = [
    path("photo/<int:id>/", RetreivePhotoView.as_view()),
    path("photo/actions/<int:id>", UpdateDeletePhotoView.as_view()),
    path("comments/<int:id>/", RetreiveCommentView.as_view()),
    path("comments/", PostCommentView.as_view()),
    path("like/", LikePostView.as_view()),
    path("photos/", ListCreatePhotoView.as_view()),
    path("users/<int:id>/", UserShowView.as_view()),
    path("users/photos/<int:id>/", ListUserPhotoView.as_view()),
    path("users/register", RegisterUserView.as_view()),
]
