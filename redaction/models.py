# redaction/models.py
import uuid
from django.db import models

def redaction_orig_path(instance, filename):
    return f'redaction/originals/{uuid.uuid4()}_{filename}'

def redaction_out_path(instance, filename):
    return f'redaction/redacted/{uuid.uuid4()}_{filename}'

class RedactionTask(models.Model):
    """
    A redaction request for a file. Can store original and redacted file paths.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    original_file = models.FileField(upload_to=redaction_orig_path)
    redacted_file = models.FileField(upload_to=redaction_out_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_msg = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title or f"RedactionTask {self.id}"


class RedactionRegion(models.Model):
    """
    Coordinates are in PDF points / pixels depending on backend.
    - page_number: 1-indexed page
    - x, y, width, height: coordinates relative to page (PDF coordinates)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(RedactionTask, on_delete=models.CASCADE, related_name='regions')
    page_number = models.PositiveIntegerField(default=1)
    x = models.FloatField()       # left
    y = models.FloatField()       # top
    width = models.FloatField()
    height = models.FloatField()
    label = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"Region p{self.page_number} ({self.x},{self.y},{self.width},{self.height})"
