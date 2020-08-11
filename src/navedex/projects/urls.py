from django.urls import path
from navedex.projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectAPIView.as_view(), name='index'),
    path('<int:id>/', views.ProjectDetailAPIView.as_view(), name='detail')
]
