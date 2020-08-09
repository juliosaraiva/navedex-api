from django.urls import path
from navedex.core import views

app_name = 'core'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]