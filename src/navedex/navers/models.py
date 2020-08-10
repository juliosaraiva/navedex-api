from django.db import models
from django.conf import settings


class Naver(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    admission_date = models.DateField()
    job_role = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
