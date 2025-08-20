# backend/video_app/views_origin.py
import os
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound
from utils.sign import verify_stream_token

def serve_hls(request, video_id, filename):
    token = request.GET.get("token")
    data = verify_stream_token(token) if token else None
    if not data or int(data.get("vid", -1)) != int(video_id):
        return HttpResponseForbidden("Invalid or missing token")

    # Only allow files inside media/hls/<video_id>/*
    base_dir = os.path.join(settings.MEDIA_ROOT, "hls", str(video_id))
    file_path = os.path.normpath(os.path.join(base_dir, filename))
    if not file_path.startswith(os.path.abspath(base_dir)):
        return HttpResponseForbidden("Path traversal detected")

    if not os.path.exists(file_path):
        return HttpResponseNotFound("Not found")

    return FileResponse(open(file_path, "rb"))
