from django.db import models
from django.conf import settings

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in seconds", null=True, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/', default='videos/default.mp4')
    hls_path = models.CharField(max_length=500, blank=True, null=True)
    thumbnails = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[("pending", "Pending"), ("processing", "Processing"), ("ready", "Ready"), ("failed", "Failed")],
        default="pending"
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    entitlement = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title