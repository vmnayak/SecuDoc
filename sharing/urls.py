# sharing/urls.py
from django.urls import path
from . import views

app_name = 'sharing'
urlpatterns = [
    # path('create/<int:document_id>/', views.create_share, name='create_share'),
    path('create/<uuid:document_id>/', views.create_share, name='create_share'),
    path('detail/<uuid:share_id>/', views.share_detail, name='share_detail'),
    path('access/<path:token>/', views.access_shared_document, name='access_shared_document'),
]
