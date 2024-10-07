from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo

class ShowPhotoService(ServiceWithResult):
    id=forms.IntegerField(required=True,min_value=1)
    def process(self):
        self.result = self._photo()
        return self
    
    def _photo(self):
        return Photo.objects.get(id=self.clean_data['id'])
