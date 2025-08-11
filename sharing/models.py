# sharing/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from documents.models import Document

class DocumentShare(models.Model):
    """
    Represents sharing of a document with a user or via email link.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shares_made')

    # Either to a registered user...
    shared_with_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='shares_received', null=True, blank=True
    )
    # ... or to an email address (guest user)
    shared_with_email = models.EmailField(null=True, blank=True)

    can_view = models.BooleanField(default=True)
    can_download = models.BooleanField(default=False)

    share_token = models.CharField(max_length=255, unique=True, blank=True, null=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        if self.shared_with_user:
            return f"{self.document.title} → {self.shared_with_user.username}"
        return f"{self.document.title} → {self.shared_with_email or 'Public'}"
