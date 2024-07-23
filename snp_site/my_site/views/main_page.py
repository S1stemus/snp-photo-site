from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
from models_app.models import Photo



class MainPageView(CreateView):
    model=Photo
    template_name="main_page.html"
    fields = ['user','photo', 'caption']
    success_url = '/'