import ast
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from navedex.projects.models import Project
from navedex.projects.serializers import (
    ProjectSerializer,
)


PROJECT_URL = reverse('project:index')


def sample_project(owner, **params):
    """Create and return a sample project"""
    defaults = dict(
        name="New WebSite Prototype"
    )
    defaults.update(params)
    return Project.objects.create(owner=owner, **params)


class PublicProjectApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving projects"""
        res = self.client.get(PROJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProjectsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = get_user_model().objects.create_user(
            email='contato@navedex.com.br',
            password='supersenha'
        )
        payload = dict(
            email='contato@navedex.com.br',
            password='supersenha'
        )
        self.login = self.client.post(PROJECT_URL, payload)
        token = ast.literal_eval(self.login.data['token'])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')

    def test_retrieve_projects(self):
        """Test that user logged successful"""
        sample_project(owner=self.owner)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_projects_limited_to_user(self):
        """Test retrieving projects for user"""
        owner2 = get_user_model().objects.create_user(
            'other@navedex.com.br',
            '12345678'
        )
        sample_naver(owner=owner2)
        sample_naver(owner=self.owner)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.filter(owner=self.owner)
        serializer = ProjectSerializer(projects, many=True)

        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
