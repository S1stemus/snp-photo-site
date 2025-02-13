from django import forms
from models_app.models import User
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class UserShowService(ServiceWithResult):
    user_id = forms.IntegerField(required=True, min_value=1)
    current_user = ModelField(User, required=False)

    custom_validations = ["_validate_user_id"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._user_id
        return self

    @property
    def _user_id(self):
        user = User.objects.get(id=self.cleaned_data["user_id"])
        print(user.username)
        return user

    def _validate_user_id(self):
        if not User.objects.filter(id=self.cleaned_data["user_id"]).exists():
            self.add_error("user_id", "Пользователь не найден")
