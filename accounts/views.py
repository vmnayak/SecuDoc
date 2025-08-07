from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import EmailOTP,User
from django.contrib import messages
from django.shortcuts import get_object_or_404



def send_otp_to_email(user):
    otp = EmailOTP.generate_otp()
    EmailOTP.objects.create(user=user, otp_code=otp)
    
    subject = 'SecuDoc Email Verification OTP'
    message = f'Your OTP for verifying your email is: {otp}'
    send_mail(subject, message, 'nadim.dp19@gmail.com', [user.email])

def resend_otp_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_verified:
        return redirect('login')

    # Mark previous OTPs as used
    EmailOTP.objects.filter(user=user, is_used=False).update(is_used=True)

    # Send a new OTP
    send_otp_to_email(user)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_email', user_id=user.id)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Block login until verified
            user.save()
            send_otp_to_email(user)
            return redirect('verify_email', user_id=user.id)
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_verified:
                error = 'Please verify your email first.'
            else:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'error': error})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def verify_email_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user, otp_code=entered_otp, is_used=False).last()
        if otp_obj and not otp_obj.is_expired():
            otp_obj.is_used = True
            otp_obj.save()
            user.is_verified = True
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'accounts/verify_email.html', {'error': 'Invalid or expired OTP'})
    return render(request, 'accounts/verify_email.html')
