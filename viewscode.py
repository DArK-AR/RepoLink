from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage
from django.conf import settings
import datetime

from .serializers import UploadFormSerializer

class GenerateUploadURL(CreateAPIView):
    serializer_class = UploadFormSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data["title"]
        file = serializer.validated_data.get("file")  # optional direct upload

        # Initialize GCS client
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)

        # File path in bucket
        blob_name = f"videos/{title}_{datetime.datetime.utcnow().isoformat()}.mp4"
        blob = bucket.blob(blob_name)

        # Generate signed URL for PUT upload
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="PUT",
            content_type="video/mp4",
        )

        return Response({
            "upload_url": url,
            "file_path": blob_name,
            "uploaded_file": file.name if file else None
        }, status=status.HTTP_201_CREATED)
