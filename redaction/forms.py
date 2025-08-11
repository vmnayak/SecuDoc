# redaction/forms.py
from django import forms
from .models import RedactionTask, RedactionRegion

class RedactionTaskForm(forms.ModelForm):
    class Meta:
        model = RedactionTask
        fields = ['title', 'original_file']

class RedactionRegionForm(forms.ModelForm):
    class Meta:
        model = RedactionRegion
        fields = ['page_number', 'x', 'y', 'width', 'height', 'label']
