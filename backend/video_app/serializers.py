from django.conf import settings
from urllib.parse import urljoin
from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['uploader']

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url  # Fallback if request is None
        return None