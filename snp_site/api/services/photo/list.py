from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from models_app.models.photo.fsm import State
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from django.conf import settings
from django.db.models import Q
from django.db import models





class ListPhotoService(ServiceWithResult):

    class SortFields(models.TextChoices):
        CREATED_AT='created_at','По дате создания'
        POPULARITY='popularity','По популярности'
        COMMENT_COUNT='comment_count','По количеству комментариев'

    page = forms.IntegerField(min_value=1, required=False)
    per_page = forms.IntegerField(min_value=1, required=False)

    sort_field=forms.ChoiceField(choices=SortFields, required=False)
    sort_direction=forms.ChoiceField(choices=(('asc', 'asc'), ('desc', 'desc')), required=False)

    search_field=forms.CharField(required=False)
    


    def process(self) -> "ServiceWithResult":      
        if self.is_valid():
            self.result = self._photos
        return self
    
    @property
    def _photos(self):
        try:
            return Paginator(
                self._filtered_photos,
                self.cleaned_data.get("per_page")
                or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data.get("page") or 1)
        except EmptyPage:
            return Paginator(
                Photo.objects.none(),
                self.cleaned_data.get("per_page")
                or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)

    @property
    def _filtered_photos(self):
        photos = Photo.objects.filter(state=State.APPROVED).annotate(comment_count = Count('model_relation')).annotate(like_count=Count('like')).select_related('user')


        if self.cleaned_data.get('search_field'):
            photos=photos.filter(
                Q(name__icontains=self.cleaned_data['search_field'])|
                Q(user__username__icontains=self.cleaned_data['search_field'])|
                Q(description__icontains=self.cleaned_data['search_field'])
                )
        sorting='' if self.cleaned_data.get('sort_direction') == 'asc' else '-'
        if self.cleaned_data.get('sort_field') == 'popularity':
            photos = photos.order_by(f'{sorting}like_count')          
        elif self.cleaned_data.get('sort_field') == 'created_at':
            photos = photos.order_by(f'{sorting}created_at')
        elif self.cleaned_data.get('sort_field') == 'comment_count':
            photos = photos.order_by(f'{sorting}comment_count')
        
        return photos
        

    