# video_app/urls.py
from django.urls import path
from .views import VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView, VideoViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'videos', VideoViewSet)

urlpatterns = [
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('videos/create/', VideoCreateView.as_view(), name='video-create'),
    path('videos/<int:pk>/update/', VideoUpdateView.as_view(), name='video-update'),
    path('videos/<int:pk>/delete/', VideoDeleteView.as_view(), name='video-delete'),
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
