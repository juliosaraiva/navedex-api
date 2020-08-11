from django.urls import path
from navedex.navers import views

app_name = 'navers'

urlpatterns = [
    path('', views.NaverAPIView.as_view(), name='index'),
    path('<int:id>/', views.NaverDetailAPIView.as_view(), name='detail')
]
