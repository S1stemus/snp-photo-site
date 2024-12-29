from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from service_objects.errors import NotFound
from models_app.models.user import User
from service_objects.fields import ModelField
from models_app.models.photo.fsm import State



class CreatePhotoService(ServiceWithResult):
    
    photo = forms.ImageField(required=True)
    description = forms.CharField(max_length=127, required=False)   
    name = forms.CharField(max_length=127, required=False) 
    current_user = ModelField(User)

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_photo
        return self
    @property
    def _create_photo(self):
        photo = Photo.objects.create(user=self.cleaned_data['current_user'],
                                     photo=self.cleaned_data['photo'],
                                     description=self.cleaned_data['description'],
                                     name =self.cleaned_data['name']
                                     )
        return photo

 