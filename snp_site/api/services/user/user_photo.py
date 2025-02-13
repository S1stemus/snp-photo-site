from django import forms
from django.conf import settings
from django.contrib.postgres.forms import SimpleArrayField
from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.db.models import Count
from models_app.models import User
from models_app.models.photo.fsm import State
from models_app.models.photo.models import Photo
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class UserPhotoService(ServiceWithResult):
    class SortFields(models.TextChoices):
        CREATED_AT = "created_at", "По дате создания"
        POPULARITY = "popularity", "По популярности"
        COMMENT_COUNT = "comment_count", "По количеству комментариев"

    user_id = forms.IntegerField(min_value=1)
    current_user = ModelField(User, required=False)

    page = forms.IntegerField(min_value=1, required=False)
    per_page = forms.IntegerField(min_value=1, required=False)

    sort_field = forms.ChoiceField(choices=SortFields, required=False)
    sort_direction = forms.ChoiceField(
        choices=(("asc", "asc"), ("desc", "desc")), required=False
    )

    state = SimpleArrayField(forms.ChoiceField(choices=State), required=False)

    custom_validations = ["_validate_user"]

    def _validate_user(self):
        if not User.objects.filter(id=self.cleaned_data["user_id"]).exists():
            self.add_error("user", "Пользователь не найден")

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._user_photos
        return self

    @property
    def _user_photos(self):
        try:
            return Paginator(
                self._filtered_user_photos,
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
    def _filtered_user_photos(self):
        photo = (
            Photo.objects.filter(user=self.cleaned_data["user_id"])
            .annotate(comment_count=Count("model_relation"))
            .annotate(like_count=Count("like"))
        )

        sorting = "" if self.cleaned_data.get("sort_direction") == "asc" else "-"
        if self.cleaned_data.get("sort_field") == "popularity":
            photo = photo.order_by(f"{sorting}like_count")
        elif self.cleaned_data.get("sort_field") == "created_at":
            photo = photo.order_by(f"{sorting}created_at")
        elif self.cleaned_data.get("sort_field") == "comment_count":
            photo = photo.order_by(f"{sorting}comment_count")

        if (
            User.objects.get(id=self.cleaned_data["user_id"])
            != self.cleaned_data["current_user"]
        ):
            return photo.filter(state=State.APPROVED)
        if self.cleaned_data.get("state"):
            photo = photo.filter(state__in=self.cleaned_data["state"])

        return photo
