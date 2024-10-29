from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from models_app.models.photo.fsm import State
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from django.conf import settings


class ListPhotoService(ServiceWithResult):

    page = forms.IntegerField(min_value=1, required=False)
    per_page = forms.IntegerField(min_value=1, required=False)

    sort_field=forms.ChoiceField(choices=(('created_at', 'created_at'),('popularity', 'popularity')), required=False)
    sort_direction=forms.ChoiceField(choices=(('asc', 'asc'), ('desc', 'desc')), required=False)


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
        photo = Photo.objects.filter(state=State.APPROVED)
        if self.cleaned_data['sort_field'] == 'popularity':
            if self.cleaned_data['sort_direction'] == 'asc':
                photo = photo.annotate(like_count=Count('like')).order_by('like_count')
            else:
                photo = photo.annotate(like_count=Count('like')).order_by('-like_count')
        elif self.cleaned_data['sort_field'] == 'created_at':
            if self.cleaned_data['sort_direction'] == 'asc':
                photo = photo.order_by('created_at')
            else:
                photo = photo.order_by('-created_at')

        return photo
        

    