from django.urls import include, path
from my_site.views.comment_view import CommentView
from my_site.views.jwt_view import JwtView
from my_site.views.like_view import LikeView
from my_site.views.main_page import MainPageView
from my_site.views.photo_list import PhotoListView
from my_site.views.photo_page import PhotoPageView
from my_site.views.register_view import RegisterView
from my_site.views.update_view import UpdatePageView
from my_site.views.user_view import UserView

urlpatterns = [
    path("photos/create/", MainPageView.as_view(), name="main_page"),
    path("photos/", PhotoListView.as_view(), name="photo_list"),
    path("photos/<pk>/", PhotoPageView.as_view(), name="photo_page"),
    path("users/", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("like/<pk>/", LikeView.as_view(), name="like"),
    path("comments/create/<pk>/", CommentView.as_view(), name="comment"),
    path("users/page/<int:pk>/", UserView.as_view(), name="user_page"),
    path("jwt/", JwtView.as_view(), name="jwt"),
    path("photos/update/<pk>/", UpdatePageView.as_view(), name="photo_update"),
]
