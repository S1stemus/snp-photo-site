

from django.views.generic import ListView
from models_app.models import Photo

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo_list_page.html'