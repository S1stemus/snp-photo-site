

from django.views.generic import ListView
from models_app.models import Photo
from models_app.models import Comment
from django.shortcuts import render

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo_list_page.html'
    paginate_by = 5
   