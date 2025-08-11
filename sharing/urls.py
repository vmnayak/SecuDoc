# sharing/urls.py
from django.urls import path
from . import views

app_name = 'sharing'
urlpatterns = [
    # path('create/<int:document_id>/', views.create_share, name='create_share'),
    path('create/<uuid:document_id>/', views.create_share, name='create_share'),
    path('detail/<uuid:share_id>/', views.share_detail, name='share_detail'),
    path('access/<path:token>/', views.access_shared_document, name='access_shared_document'),
    path('shared-with-me/', views.shared_with_me, name='shared_with_me'),
    path('open/<uuid:share_id>/', views.open_shared_document, name='open_shared_document'),
    path('delete/<uuid:share_id>/', views.delete_shared_document, name='delete_shared_document'),
]
