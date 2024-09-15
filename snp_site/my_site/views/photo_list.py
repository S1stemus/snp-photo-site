

from django.views.generic import ListView
from models_app.models import Photo
from models_app.models import Comment
from django.shortcuts import render




class PhotoListView(ListView):
    model = Photo
    template_name = 'photo_list_page.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter=self.request.GET.get('filter')
        photos=Photo.objects.filter(status='Опубликован')
        if filter=='old':
            photos=sorted(photos, key=lambda x: x.created_at)
        elif filter=='new':
            photos=sorted(photos, key=lambda x: x.created_at, reverse=True)
        elif filter=='popular':
            photos=sorted(photos, key=lambda x: x.likes.count(), reverse=True)
        context['photos']=photos
        return context
   