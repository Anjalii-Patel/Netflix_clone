from django.conf import settings
from urllib.parse import urljoin
from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    playback_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['uploader']

    def get_playback_url(self, obj):
        request = self.context.get('request')
        if obj.hls_path:
            # Build absolute URL to master.m3u8
            rel_url = f"/media/{obj.hls_path}"
            if request:
                return request.build_absolute_uri(rel_url)
            return rel_url
        return None
