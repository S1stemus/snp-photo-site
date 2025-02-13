from django import forms
from models_app.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from service_objects.services import ServiceWithResult


class CreateUserService(ServiceWithResult):
    username = forms.CharField(max_length=127)
    password = forms.CharField(max_length=127)
    avatar = forms.ImageField(required=False)

    def process(self):
        self.result = self._create_user
        return self

    @property
    def _create_user(self):
        user = User(
            username=self.cleaned_data["username"],
            avatar=self.cleaned_data["avatar"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        # Генерация токенов
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
