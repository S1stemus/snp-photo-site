import factory
from models_app.models import Like
from faker import Faker

faker=Faker()

class LikeFactory(factory.django.DjangoModelFactory):
    photo=factory.SubFactory('models_app.factories.photo.PhotoFactory')
    user=factory.SubFactory('models_app.factories.user.UserFactory')
    class Meta:
        model= Like