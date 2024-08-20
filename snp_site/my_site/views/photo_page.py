from django.views.generic import DetailView
from models_app.models import Photo
class PhotoPageView(DetailView):
    model = Photo
    template_name = 'photo_page.html'
    context_object_name = 'photo'