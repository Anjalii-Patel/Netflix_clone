from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Video
from .serializers import VideoSerializer
import subprocess, os

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.filter(status='ready')
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.filter(status='ready')
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

# class VideoCreateView(generics.CreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = [permissions.IsAdminUser]

#     def perform_create(self, serializer):
#         serializer.save(uploader=self.request.user)

class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Save initial video with "pending" status
        video = serializer.save(uploader=self.request.user, status="pending")
        input_path = video.file.path

        # Prepare output directory for HLS
        output_dir = os.path.join("media/hls", str(video.id))
        os.makedirs(output_dir, exist_ok=True)

        # Update to "processing"
        video.status = "processing"
        video.save(update_fields=["status"])

        # Run ffmpeg (sync for now)
        output_variant = os.path.join(output_dir, "720p.m3u8")
        cmd = [
            "ffmpeg", "-i", input_path,
            "-c:v", "libx264", "-b:v", "1500k", "-s", "1280x720",
            "-c:a", "aac", "-f", "hls",
            "-hls_time", "6", "-hls_playlist_type", "vod",
            output_variant,
        ]
        subprocess.run(cmd, check=True)

        # Create master.m3u8 playlist
        master_path = os.path.join(output_dir, "master.m3u8")
        with open(master_path, "w") as f:
            f.write('#EXTM3U\n')
            f.write('#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=1280x720\n')
            f.write("720p.m3u8\n")

        # Update hls_path and status
        video.hls_path = master_path.replace("media/", "")  # relative path for serving
        video.status = "ready"
        video.save(update_fields=["hls_path", "status"])

class VideoUpdateView(generics.UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAdminUser]

class VideoDeleteView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    permission_classes = [permissions.IsAdminUser]

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context