from django.urls import path
from my_site.views.main_page import MainPageView
from django.conf import settings

from my_site.views.photo_list import PhotoListView
urlpatterns = [ 

    path('', MainPageView.as_view(), name="main_page"),
    path('photolist', PhotoListView.as_view(), name="photo_list"),
    
]
