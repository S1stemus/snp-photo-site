

from django.views.generic import ListView
from models_app.models import Photo
from models_app.models import Comment

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo_list_page.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos']=Photo.objects.all()
        photos=Photo.objects.all()
        for photo in photos:            
            print(photo.model_relation.all())
        return context