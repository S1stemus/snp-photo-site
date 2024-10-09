
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Comment

class RetrieveCommentsByIdService(ServiceWithResult):
    id = forms.IntegerField(required=True, min_value=1)

    custom_validations = ['_validate_comment_id']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment()
        return self

    def _comment(self):
        return Comment.objects.get(id=self.cleaned_data['id'])

    def _validate_comment_id(self):
        if not Comment.objects.filter(id=self.cleaned_data['id']).exists() or not self.cleaned_data['id']:
            self.add_error('id', 'Комментарий не найден или не дан')