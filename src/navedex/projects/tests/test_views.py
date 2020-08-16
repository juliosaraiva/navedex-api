from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from navedex.projects.models import Project
from navedex.projects.serializers import (
    ProjectSerializer,
    ProjectCreateSerializer,
    ProjectDetailSerializer
)

from navedex.navers.models import Naver


PROJECT_URL = reverse('projects:project-list')
TOKEN_URL = reverse('core:login')


def detail_url(project_id):
    return reverse('projects:project-detail', args=[project_id])


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
        self.login = self.client.post(TOKEN_URL, payload)
        token = self.login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

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
        sample_project(owner=owner2)
        sample_project(owner=self.owner)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.filter(owner=self.owner)
        serializer = ProjectSerializer(projects, many=True)

        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_creating_project_sucessful(self):
        """Test creating a new project successfully"""
        payload = dict(
            name="Web Site Prototype"
        )
        self.client.post(PROJECT_URL, payload)

        exists = Project.objects.filter(
            owner=self.owner, name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_project_invalid(self):
        payload = {"name": ""}
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_project_by_name(self):
        """Test filtering project by name"""
        p1 = {'name': 'new Web Site Prototype'}
        p2 = {'name': 'New Logo'}

        project1 = sample_project(owner=self.owner, **p1)
        project2 = sample_project(owner=self.owner, **p2)

        res = self.client.get(PROJECT_URL, {'name': p1['name']})

        serializer1 = ProjectSerializer(project1)
        serializer2 = ProjectSerializer(project2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_view_project_detail(self):
        """Test that can add naver to project"""
        naver_dict = {'name': 'Naver 1', 'birthdate': '1991-01-01',
                      'admission_date': '2020-08-10', 'job_role': 'Tech Leader'}
        naver = Naver.objects.create(owner=self.owner, **naver_dict)

        project = Project.objects.create(
            owner=self.owner, name="New WebSite Prototype"
        )
        project.navers.add(naver)

        url = detail_url(project.id)
        res = self.client.get(url, args=[project.id])
        serializer = ProjectDetailSerializer(project)

        self.assertEqual(serializer.data, res.data)

    def test_create_project_with_naver(self):
        """Test that can create a project with naver"""
        naver_dict = {'name': 'Naver 1', 'birthdate': '1991-01-01',
                      'admission_date': '2020-08-10', 'job_role': 'Tech Leader'}
        naver = Naver.objects.create(owner=self.owner, **naver_dict)
        payload = {'name': 'Website Prototype', 'navers': [naver.id]}

        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        project = Project.objects.get(id=res.data['id'])
        serializer = ProjectCreateSerializer(project)

        self.assertEqual(serializer.data, res.data)
