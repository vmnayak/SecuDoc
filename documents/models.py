# documents/models.py

import uuid
from django.db import models
from django.conf import settings

def original_document_path(instance, filename):
    return f'documents/originals/{instance.owner.id}/{uuid.uuid4()}_{filename}'

def redacted_document_path(instance, filename):
    return f'documents/redacted/{instance.owner.id}/{uuid.uuid4()}_{filename}'

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_documents'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=original_document_path)

    file_type = models.CharField(max_length=50, choices=[
        ('pdf', 'PDF'),
        ('image', 'Image'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    is_encrypted = models.BooleanField(default=False)
    encryption_key = models.CharField(max_length=256, blank=True, null=True)

    is_redacted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class RedactedDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original = models.OneToOneField(
        Document, on_delete=models.CASCADE, related_name='redacted_version'
    )
    redacted_file = models.FileField(upload_to=redacted_document_path)
    redacted_at = models.DateTimeField(auto_now_add=True)
    redacted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='redactions_done'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Redacted: {self.original.title}"

    class Meta:
        ordering = ['-redacted_at']
