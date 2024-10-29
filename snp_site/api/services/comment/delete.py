from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Comment
from service_objects.errors import NotFound

class DeleteCommentService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    custom_validations = [
        '_validate_comment_id'
    ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_comment
        return self

    @property
    def _delete_comment(self):
        try:
            com= Comment.objects.get(id=self.cleaned_data['id'])
            com.delete()
            return com
        except Comment.DoesNotExist:
            return None

    def _validate_comment_id(self):
        if not self._delete_comment:
            self.add_error('id', NotFound(message=f'Комментарий с id {self.cleaned_data["id"]} не найден'))