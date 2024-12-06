
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Comment
from service_objects.errors import NotFound 
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings

class RetrieveCommentsByIdService(ServiceWithResult):
    id = forms.IntegerField(required=True, min_value=1)

    page = forms.IntegerField(min_value=1, required=False)
    per_page = forms.IntegerField(min_value=1, required=False)


    custom_validations = ['_validate_comment_id']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment
        return self
    
    @property
    def _comment(self):
        try:
            return Paginator(
                self._filtered_comments,
                self.cleaned_data.get("per_page")
                or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data.get("page") or 1)
        except EmptyPage:
            return Paginator(
                Comment.objects.none(),
                self.cleaned_data.get("per_page")
                or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)

    @property
    def _filtered_comments(self):
            return Comment.objects.filter(object_id=self.cleaned_data['id'])          

    def _validate_comment_id(self):
        if not Comment.objects.filter(object_id=self.cleaned_data['id']).exists():
            self.add_error('id',NotFound(message = f'Объект {self.cleaned_data["id"]} не найден '))