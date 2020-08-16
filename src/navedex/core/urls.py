from django.urls import path
from navedex.core import views

app_name = 'core'

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='login'),
]
