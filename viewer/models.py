# viewer/models.py

from django.db import models
from django.conf import settings
from documents.models import Document
from django.utils import timezone

class DocumentViewLog(models.Model):
    share = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='view_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(default=timezone.now)
    session_id = models.CharField(max_length=64, blank=True)  # Optional

    def __str__(self):
        return f"{self.user} viewed {self.share.title} at {self.viewed_at}"
