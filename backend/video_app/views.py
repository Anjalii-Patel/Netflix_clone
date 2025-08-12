from django.shortcuts import render
from rest_framework import generics, permissions
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

class VideoUpdateView(generics.UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAdminUser]

class VideoDeleteView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    permission_classes = [permissions.IsAdminUser]
