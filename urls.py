from django.urls import path
from .views import VideoUploadView

urlpatterns = [
    path("api/", VideoUploadView.as_view(), name="upload_video"),
]
