from django.contrib import admin
from .models import Document, RedactedDocument
# Register your models here.
admin.site.register(Document)
admin.site.register(RedactedDocument)
