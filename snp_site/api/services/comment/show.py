
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Comment
from service_objects.errors import NotFound 

class RetrieveCommentsByIdService(ServiceWithResult):
    id = forms.IntegerField(required=True, min_value=1)

    custom_validations = ['_validate_comment_id']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _comment(self):
        try:
            return Comment.objects.filter(object_id=self.cleaned_data['id'])
        except Comment.DoesNotExist:
            return None

    def _validate_comment_id(self):
        if not Comment.objects.filter(id=self.cleaned_data['id']).exists():
            self.add_error('id',NotFound(message = f'Объект {self.cleaned_data["id"]} не найден '))