import ast
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from navedex.navers.models import Naver
from navedex.navers.serializers import NaverSerializer

TOKEN_URL = reverse('core:login')
NAVERS_URL = reverse('navers:retrieve')


def sample_naver(owner, **params):
    """Create and return a sample naver"""
    defaults = dict(
        name="New User",
        birthdate="2020-08-10",
        admission_date="2020-09-01",
        job_role="Developer"
    )
    defaults.update(params)
    return Naver.objects.create(owner=owner, **defaults)


class PublicNaverAPITests(TestCase):
    """Test unauthenticated naver API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(NAVERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNaverAPITest(TestCase):
    """Test authenticated navers API request"""

    def setUp(self):
        self.client = APIClient()
        self.owner = get_user_model().objects.create_user(
            'suporte@navedex.com.br',
            'supersenha'
        )
        payload = dict(
            email='suporte@navedex.com.br',
            password='supersenha'
        )
        self.login = self.client.post(TOKEN_URL, payload)
        token = ast.literal_eval(self.login.data["token"])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')

    def test_retrieve_navers(self):
        """Test that is authenticated and authorized"""
        sample_naver(owner=self.owner)

        res = self.client.get(NAVERS_URL)

        navers = Naver.objects.all().order_by('-id')
        serializer = NaverSerializer(navers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_navers_limited_to_user(self):
        """Test retrieving navers for user"""
        owner2 = get_user_model().objects.create_user(
            'other@navedex.com.br',
            'passtest'
        )
        sample_naver(owner=owner2)
        sample_naver(owner=self.owner)

        res = self.client.get(NAVERS_URL)

        navers = Naver.objects.filter(owner=self.owner)
        serializer = NaverSerializer(navers, many=True)

        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
