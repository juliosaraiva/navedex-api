from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from navedex.navers.models import Naver
from navedex.navers.serializers import (
    NaverSerializer,
    NaverCreateSerializer,
    NaverDetailSerializer
)

from navedex.projects.models import Project

TOKEN_URL = reverse('core:login')
NAVERS_URL = reverse('navers:naver-list')


def detail_url(naver_id):
    return reverse('navers:naver-detail', args=[naver_id])


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
        token = self.login.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

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

    def test_create_naver_successful(self):
        """Test creating a new tag successfully"""
        payload = dict(
            name="Test User",
            birthdate="1985-10-10",
            admission_date="2020-01-01",
            job_role="Manager"
        )
        self.client.post(NAVERS_URL, payload)
        exists = Naver.objects.filter(
            owner=self.owner,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_naver_invalid(self):
        payload = dict(name="", birthdate="", admission_date="", job_role="")
        res = self.client.post(NAVERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_navers_by_name(self):
        """Test filtering navers by name"""
        n1 = {'name': 'Naver 1', 'birthdate': '1991-01-01',
              'admission_date': '2020-08-10', 'job_role': 'Tech Leader'}
        n2 = {'name': 'Naver 2', 'birthdate': '1992-02-02',
              'admission_date': '2020-09-11', 'job_role': 'Designer'}

        naver1 = sample_naver(owner=self.owner, **n1)
        naver2 = sample_naver(owner=self.owner, **n2)

        res = self.client.get(NAVERS_URL, {'name': n1['name']})

        serializer1 = NaverSerializer(naver1)
        serializer2 = NaverSerializer(naver2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_navers_by_admission_date(self):
        """Test filtering navers by admission date"""
        n1 = {'name': 'Naver 1', 'birthdate': '1991-01-01',
              'admission_date': '2020-08-10', 'job_role': 'Tech Leader'}
        n2 = {'name': 'Naver 2', 'birthdate': '1992-02-02',
              'admission_date': '2020-09-11', 'job_role': 'Designer'}

        naver1 = sample_naver(owner=self.owner, **n1)
        naver2 = sample_naver(owner=self.owner, **n2)

        res = self.client.get(NAVERS_URL, {'admission_date': n1['admission_date']})

        serializer1 = NaverSerializer(naver1)
        serializer2 = NaverSerializer(naver2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_navers_by_job_role(self):
        """Test filtering navers by Job Role"""
        n1 = {'name': 'Naver 1', 'birthdate': '1991-01-01',
              'admission_date': '2020-08-10', 'job_role': 'Tech Leader'}
        n2 = {'name': 'Naver 2', 'birthdate': '1992-02-02',
              'admission_date': '2020-09-11', 'job_role': 'Designer'}

        naver1 = sample_naver(owner=self.owner, **n1)
        naver2 = sample_naver(owner=self.owner, **n2)

        res = self.client.get(NAVERS_URL, {'job_role': n1['job_role']})

        serializer1 = NaverSerializer(naver1)
        serializer2 = NaverSerializer(naver2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_naver_with_project(self):
        """Test that can add project to naver"""
        project = Project.objects.create(
            name="New Website Prototype",
            owner=self.owner
        )

        payload = dict(
            name='Naver 2',
            birthdate='1992-02-02',
            admission_date='2020-09-11',
            job_role='Designer',
            projects=[project.id]
        )
        res = self.client.post(NAVERS_URL, payload)

        naver = Naver.objects.get(id=res.data["id"])
        serializer = NaverCreateSerializer(naver)

        self.assertEqual(serializer.data, res.data)

    def test_remove_naver_successful(self):
        """Test that the owner can remove a naver successfully"""
        naver_dict = dict(
            name='Naver 1',
            birthdate='1992-02-02',
            admission_date='2020-09-11',
            job_role='Designer',
        )
        n1 = sample_naver(owner=self.owner, **naver_dict)

        url = detail_url(n1.id)
        res = self.client.delete(url)

        naver = Naver.objects.filter(id=n1.id).exists()

        self.assertFalse(naver)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_partial_update_naver(self):
        """Test updating a naver with a PATCH method"""
        n1 = dict(
            name='Naver 1',
            birthdate='1992-02-02',
            admission_date='2020-09-11',
            job_role='Designer',
        )
        naver = sample_naver(owner=self.owner, **n1)
        project = Project.objects.create(owner=self.owner, name="Develop a New API")

        payload = dict(
            job_role="Backend Developer",
            projects=[project.id]
        )

        url = detail_url(naver.id)
        self.client.patch(url, payload)

        naver.refresh_from_db()

        self.assertEqual(naver.job_role, payload['job_role'])
        projects = naver.projects.all()
        self.assertEqual(len(projects), 1)
        self.assertIn(project, projects)

    def test_full_update_naver(self):
        """Test updating a naver with PUT method"""
        naver = sample_naver(owner=self.owner)
        project = Project.objects.create(owner=self.owner, name="New Website")
        naver.projects.add(project)

        payload = dict(
            name="Naver Updated",
            birthdate="1980-12-31",
            admission_date="2050-01-01",
            job_role="UX"
        )
        url = detail_url(naver.id)
        self.client.put(url, payload)

        naver.refresh_from_db()
        self.assertEqual(naver.name, payload["name"])
        self.assertEqual(str(naver.birthdate), payload["birthdate"])
        self.assertEqual(str(naver.admission_date), payload["admission_date"])
        self.assertEqual(naver.job_role, payload["job_role"])
        projects = naver.projects.all()
        self.assertEqual(len(projects), 0)
