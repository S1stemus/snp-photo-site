import factory
from models_app.models import User
from faker import Faker

faker=Faker()

class UserFactory(factory.django.DjangoModelFactory):
    username=factory.Sequence(lambda n: f'{n}_{faker.email()}')

    class Meta:
        model=User



