from django.urls import path, include
from rest_framework.routers import DefaultRouter

from navedex.navers import views

router = DefaultRouter()
router.register('', views.NaverViewSet)


app_name = 'navers'

urlpatterns = [
    path('', include(router.urls)),
]
