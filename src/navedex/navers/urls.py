from django.urls import path
from navedex.navers import views

app_name = 'navers'

urlpatterns = [
    path('', views.NaverAPIView.as_view(), name='retrieve'),
]
