from django.contrib import admin
from django.urls import path, include
from faceChecker.views.face import hello_world 
from faceChecker.views.face import capture_photo
from faceChecker.views.face import camera_view
from faceChecker.views.face import get_face_features
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('faceChecker.urls')),
    path('', hello_world, name='home'),
    path('capture/', capture_photo, name='capture_photo'),
    path("camera/", camera_view, name="camera"),
    path('features/', get_face_features, name='get_face_features'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
