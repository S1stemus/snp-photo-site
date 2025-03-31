import factory
from models_app.models import Photo
from faker import Faker
from models_app.models.photo.fsm import State

faker=Faker()
class PhotoFactory(factory.django.DjangoModelFactory):
    user=factory.SubFactory('models_app.factories.user.UserFactory')
    name=faker.word()
    photo=factory.django.ImageField()
    description=faker.word()
    state=State.APPROVED

    class Meta:
        model= Photo
