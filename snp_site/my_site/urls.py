from atexit import register
from django.urls import path
from my_site.views.main_page import MainPageView
from django.conf import settings
from django.urls import include
from my_site.views.register_view import RegisterView
from my_site.views.photo_page import PhotoPageView
from my_site.views.photo_list import PhotoListView
urlpatterns = [ 

    path('photos/create/', MainPageView.as_view(), name="main_page"),
    path('photos/', PhotoListView.as_view(), name="photo_list"),
    path('photos/<pk>/', PhotoPageView.as_view(), name="photo_page"),
    path('users/',include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name="register"),
]
