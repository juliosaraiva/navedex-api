from django.db import models
from django.conf import settings


class Naver(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    admission_date = models.DateField()
    job_role = models.CharField(max_length=255)
    projects = models.ManyToManyField('projects.Project')

    def __str__(self):
        return self.name
