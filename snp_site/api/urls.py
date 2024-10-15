from api.views.photo import RetreivePhotoView
from api.views.comment import RetreiveCommentView
from django.urls import path
from api.views.comment import RetreiveCommentView
from api.services.like.create import CreateLikeService
from api.views.like import LikePostView


urlpatterns=[
    path('photo/<int:id>/', RetreivePhotoView.as_view()),
    path('comments/<int:id>/', RetreiveCommentView.as_view()),
    path('like', LikePostView.as_view()),
]
