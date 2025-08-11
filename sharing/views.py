# sharing/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.utils import timezone
from django.core.exceptions import PermissionDenied
import uuid

from .models import DocumentShare
from .forms import DocumentShareForm
from documents.models import Document
from .utils import generate_share_link, verify_share_link

@login_required
def create_share(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)
    if request.method == 'POST':
        form = DocumentShareForm(request.POST)
        if form.is_valid():
            share = form.save(commit=False)
            share.document = document
            share.shared_by = request.user
            share.share_token = str(uuid.uuid4())
            share.save()
            return redirect('sharing:share_detail', share.id)
    else:
        form = DocumentShareForm()
    return render(request, 'sharing/create_share.html', {'form': form, 'document': document})

@login_required
def share_detail(request, share_id):
    share = get_object_or_404(DocumentShare, id=share_id, shared_by=request.user)
    signed_link = generate_share_link(share.id, max_age_seconds=None)
    return render(request, 'sharing/share_detail.html', {'share': share, 'signed_link': signed_link})

def access_shared_document(request, token):
    try:
        share_id = verify_share_link(token)
    except Exception:
        raise Http404("Invalid or expired link")

    share = get_object_or_404(DocumentShare, id=share_id)

    # Check expiration
    if share.is_expired():
        raise PermissionDenied("This share link has expired.")

    # Permission checks
    if share.shared_with_user and request.user != share.shared_with_user:
        if not request.user.is_authenticated:
            return redirect('login')
        raise PermissionDenied("You do not have access to this document.")

    # Serve document securely
    document = share.document
    return render(request, 'viewer/secure_view.html', {
        'document': document,
        'username': request.user.username if request.user.is_authenticated else 'Guest',
        'ip': request.META.get('REMOTE_ADDR'),
        'now': timezone.now(),
    })
