from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from .models import Video
from .serializers import VideoSerializer

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.filter(status='ready')
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.filter(status='ready')
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

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