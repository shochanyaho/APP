from django.urls import path
from faceChecker.views.face import hello_world

urlpatterns = [
    path('hello/', hello_world , name='hello_world'),
]
