from django.test import TestCase
from django.contrib.auth import get_user_model

from navedex.navers import models


def sample_user(email="user@navedex.com.br", password="12345678"):
    return get_user_model().objects.create_user(email, password)


class NaversModelTest(TestCase):
    def test_saving_and_retriving_navers(self):
        """Test that can saving and retriving navers"""
        naver = models.Naver.objects.create(
            name="Fulano",
            birthdate="1999-05-15",
            admission_date="2020-06-12",
            job_role="Desenvolvedor",
            owner=sample_user()
        )
        self.assertEqual(str(naver), naver.name)
