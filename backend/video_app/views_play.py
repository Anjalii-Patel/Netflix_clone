# backend/video_app/views_play.py
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Video
from users.models import Subscription
from utils.sign import gen_stream_token
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class PlayURLView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk, status="ready")
        except Video.DoesNotExist:
            return Response({"detail": "Video not found or not ready"}, status=status.HTTP_404_NOT_FOUND)

        # check subscription
        has_sub = Subscription.objects.filter(user=request.user, active=True, end_date__gt=None).exists()
        has_sub = Subscription.objects.filter(user=request.user, active=True, end_date__gt=timezone.now()).exists()
        if not has_sub:
            return Response({"detail": "Subscription required"}, status=status.HTTP_402_PAYMENT_REQUIRED)

        # compute HLS path for this video
        manifest_rel = f"hls/{video.id}/master.m3u8"

        # sign token for user+video (short TTL)
        token = gen_stream_token(request.user.id, video.id, ttl_seconds=300)

        playback_url = f"{settings.MEDIA_URL}{manifest_rel}?token={token}"
        return Response({"playback_url": request.build_absolute_uri(playback_url)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def play_url(request, pk):
    """
    Issue a playback URL only if user has subscription.
    """
    user = request.user
    has_sub = Subscription.objects.filter(
        user=user,
        active=True,
        end_date__gt=timezone.now()
    ).exists()

    if not has_sub:
        return Response({"error": "No active subscription"}, status=403)

    try:
        video = Video.objects.get(pk=pk, status="ready")
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)

    # For now just return static hls_path, later we sign it
    return Response({"play_url": video.hls_path})