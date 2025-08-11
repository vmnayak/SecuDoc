# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
import random

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)  # After OTP verification

    def __str__(self):
        return self.username


class EmailOTP(models.Model):
    """
    Stores OTP for email verification (one-time use).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp_code}"

    def is_expired(self):
        return (timezone.now() - self.created_at).seconds > 300  # valid for 5 mins

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
