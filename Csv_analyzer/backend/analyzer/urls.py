from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('csrf/', views.get_csrf_token, name='get_csrf_token')
]
