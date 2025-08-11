# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify/<int:user_id>/', views.verify_email_view, name='verify_email'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('resend-otp/<int:user_id>/', views.resend_otp_view, name='resend_otp'),

]
