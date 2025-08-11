# viewer/urls.py

from django.urls import path
from .views import secure_view_document, serve_protected_pdf

urlpatterns = [
    path('<uuid:document_id>/view/', secure_view_document, name='secure_view_document'),
   path('serve-pdf/<uuid:document_id>/', serve_protected_pdf, name='serve_protected_pdf'),
#    path('serve-pdf/<uuid:document_id>/', secure_view_document, name='secure_view_document'),
   

]
