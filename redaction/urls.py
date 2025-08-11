# redaction/urls.py
from django.urls import path
from . import views

app_name = 'redaction'
urlpatterns = [
    path('create/', views.create_task, name='create_task'),
    path('task/<uuid:task_id>/', views.task_detail, name='task_detail'),
    path('task/<uuid:task_id>/add-region/', views.add_region, name='add_region'),
    path('task/<uuid:task_id>/process/', views.process_task, name='process_task'),
]
