# viewer/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from documents.models import Document
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site

from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from django.urls import reverse

@login_required
def secure_view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    secure_pdf_url = reverse('serve_protected_pdf', args=[document.id])  # Secure URL

    return render(request, 'viewer/secure_view.html', {
        'document': document,
        'document_url': secure_pdf_url,  # ✅ pass to frontend
        'username': request.user.username,
        'ip': get_client_ip(request),
        'now': timezone.now(),
    })

# @login_required
# def secure_view_document(request, document_id):
#     document = get_object_or_404(Document, id=document_id, owner=request.user)

#     # Build absolute URL for PDF.js
#     domain = get_current_site(request).domain
#     scheme = 'https' if request.is_secure() else 'http'
#     absolute_url = f"{scheme}://{domain}{document.file.url}"
#     print(f"Absolute URL for PDF.js: {absolute_url}")

#     return render(request, 'viewer/secure_view.html', {
#         'document': document,
#         'document_url': absolute_url,
#         'username': request.user.username,
#         'ip': get_client_ip(request),
#         'now': timezone.now(),
#     })

def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')

@csrf_exempt
@login_required
def serve_protected_pdf(request, document_id):
    doc = get_object_or_404(Document, id=document_id, owner=request.user)

    file_path = doc.file.path
    if not os.path.exists(file_path):
        raise Http404

    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Access-Control-Allow-Origin'] = '*'
    return response

# @csrf_exempt
# def serve_protected_pdf(request, document_id):
#     from documents.models import Document  # or wherever your Document model is

#     try:
#         doc = Document.objects.get(id=document_id)
#         file_path = doc.file.path
#         if not os.path.exists(file_path):
#             raise Http404

#         response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
#         response['Access-Control-Allow-Origin'] = '*'
#         return response

#     except Document.DoesNotExist:
#         raise Http404