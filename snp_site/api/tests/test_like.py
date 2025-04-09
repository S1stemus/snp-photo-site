from http import client
from django.test import TestCase
from models_app.factories import UserFactory, PhotoFactory
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework.test import APIClient
from django.test.client import encode_multipart

faker=Faker()
class Liketest(TestCase):
    @classmethod
    def setUp(cls):
        cls.url = '/api/like/'
        cls.user = UserFactory()
        cls.photo = PhotoFactory(user=cls.user)
        cls.token = RefreshToken.for_user(cls.user).access_token
    def test_like_status_200(self):
        data = {
            'photo_id': self.photo.id
            }
        
        client = APIClient()
        
        response = client.post(self.url, data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)

    