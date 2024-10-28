from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from models_app.models.photo.fsm import State


class ListPhotoService(ServiceWithResult):
    filter=forms.ChoiceField(choices=(('old', 'old'), ('new', 'new'), ('popular', 'popular')), required=False)
    def process(self) -> "ServiceWithResult":      
        if self.is_valid():
            self.result = self._photos
        return self
    @property
    def _photos(self):
        return Photo.objects.filter(state=State.APPROVED)
    