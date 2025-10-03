from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import PasswordResetToken
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from accounts.models import Address
from .forms import AddressForm
from django.urls import reverse

# Create your views here.

def auth_page(request):
    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            context = {
                'show_signup': True,
                'signup_data': {
                    'username': username,
                    'email': email,
                }
            }

            if password1 != password2:
                messages.error(request,"Passwords doesn't match")
                return render(request, 'accounts/login.html', context)
            
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'accounts/login.html', context)
            
            else:
                user = User.objects.create_user(username=username, email=email,password=password1)
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('index')
            
        elif 'signin_submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            context = {
                'show_signup': False,
                'signin_data': {
                    'username': username,
                }
            }

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('index')
            
            else:
                messages.error(request, "Login failed. Check your credentials.")
                return render(request, 'accounts/login.html', context)
            
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('auth_login')


def profile(request):
    addresses = Address.objects.filter(user=request.user)
    form = AddressForm()
    context = {
        'addresses' : addresses,
        'form' : form
    }
    return render(request,'accounts/profile.html', context)


def add_address(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect('profile')
    else:
        messages.error(request, 'Something went error. Try again')
    return render(request,'accounts/profile.html')



def forgot_password(request):
    if request.method=='POST':
        email = request.POST.get('email')
        try:
            user  = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,'User not found!')
            return redirect('forgot_password')
        
        token = get_random_string(32)
        expiry = timezone.now() + timedelta(minutes=30)

        PasswordResetToken.objects.create(user=user, token=token, expiry=expiry)

        reset_link = request.build_absolute_uri(reverse("reset_password", args=[token]))
        send_mail(
            subject= "Reset your password - Liora",
            message=f"Hi {user.username},\n\nClick here to reset your password:\n{reset_link}\n\nThis link will expire in 30 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        messages.success(request, "Password reset link sent to your email.")
        return redirect('auth_login')

    return render(request, "accounts/forgot_password.html")


def reset_password(request,token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid reset link")
        return redirect("forgot_password")
    
    if not reset_token.is_valid():
        messages.error(request,"Reset link expired")
        return redirect("forgot_password")
    
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request,"Passwords do not match")
            return redirect("reset_password", token=token)
        
        user = reset_token.user
        user.password = make_password(new_password)
        user.save()

        reset_token.delete()
        messages.success(request, "Password reset successfully! You can login now")
        return redirect("auth_login")
    
    return render(request, "accounts/reset_password.html", {'token':token})