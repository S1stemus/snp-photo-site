from pdb import run
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo

class ShowPhotoService(ServiceWithResult):

    id=forms.IntegerField(required=True,min_value=1)

    custom_validations = ['_validate_photo_id']

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._photo() 
        return self
    
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data['id'])
    
    def _validate_photo_id(self):
        if not Photo.objects.filter(id=self.cleaned_data['id']).exists() or not self.cleaned_data['id']:
            self.add_error('id', 'Фото не найдено или не дано')
           