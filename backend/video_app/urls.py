from django.urls import path
from .views import (
    VideoListView, VideoDetailView, VideoCreateView,
    VideoUpdateView, VideoDeleteView,
)

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('videos/create/', VideoCreateView.as_view(), name='video-create'),
    path('videos/<int:pk>/update/', VideoUpdateView.as_view(), name='video-update'),
    path('videos/<int:pk>/delete/', VideoDeleteView.as_view(), name='video-delete'),
]
