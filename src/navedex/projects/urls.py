from django.urls import path, include
from rest_framework.routers import DefaultRouter

from navedex.projects import views

router = DefaultRouter()
router.register('', views.ProjectViewSet)

app_name = 'projects'

urlpatterns = [
    path('', include(router.urls))
]
