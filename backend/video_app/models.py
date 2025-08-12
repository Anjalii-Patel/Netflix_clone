from django.db import models
from django.conf import settings

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in seconds", null=True, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    filepath = models.CharField(max_length=500, default="")  # will store path to file (local or S3)
    thumbnails = models.CharField(max_length=500, blank=True)  # store thumbnail path or URL
    status = models.CharField(max_length=50, default="pending")  # pending, processing, ready, error
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    entitlement = models.JSONField(blank=True, null=True)  # later for access control

    def __str__(self):
        return self.title