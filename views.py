from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer

class VideoUploadView(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        video = Video.objects.get(pk=response.data["id"])
        video_url = request.build_absolute_uri(video.file.url)
        response.data["video_url"] = video_url
        return response
