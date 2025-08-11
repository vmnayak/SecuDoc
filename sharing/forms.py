# sharing/forms.py
from django import forms
from .models import DocumentShare

class DocumentShareForm(forms.ModelForm):
    class Meta:
        model = DocumentShare
        fields = ['shared_with_user', 'shared_with_email', 'can_view', 'can_download']
