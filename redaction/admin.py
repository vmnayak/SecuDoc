# redaction/admin.py
from django.contrib import admin
from .models import RedactionTask, RedactionRegion

class RegionInline(admin.TabularInline):
    model = RedactionRegion
    extra = 0

@admin.register(RedactionTask)
class RedactionTaskAdmin(admin.ModelAdmin):
    inlines = [RegionInline]
    list_display = ('title', 'created_at', 'processed')
