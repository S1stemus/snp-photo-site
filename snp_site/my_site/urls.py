from django.urls import path
from my_site.views.main_page import MainPageView
urlpatterns = [ 

    path('', MainPageView.as_view(), name="main_page"),
]