from http import client
from django.test import TestCase
from models_app.factories import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework.test import APIClient
from django.test.client import encode_multipart

faker=Faker()

class UserShowUpdateTest(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.user=UserFactory()
        cls.token=str(RefreshToken.for_user(cls.user).access_token)
        cls.url='/api/users/'
    def test_user_show_status_200(self):
        response=self.client.get(f'{self.url}{self.user.id}/')
        self.assertEqual(response.status_code,200)
        



class UserPhotosTest(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.url='/api/users/photos/'
        cls.user=UserFactory()
        token=str(RefreshToken.for_user(cls.user).access_token)
    def test_user_photos_status_200(self):
        response=self.client.get(f'/api/users/photos/{self.user.id}/')
        self.assertEqual(response.status_code,200)
    
class UserCreateTest(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.url='/api/users/register/'


    def test_create_user_status_200(self):
        data = {
            'username': 'ldfasfsdf',
            'password': 'sss',
            'photo': SimpleUploadedFile(name='test_image.png', content=faker.image((20, 20), 'png'), content_type='image/png')
        }

        client = APIClient()
        
    
        response = client.post(
            path=self.url,
            data=data,
            format='multipart',  
        )

        self.assertEqual(response.status_code, 201)

    