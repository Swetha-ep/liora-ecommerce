from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from accounts.models import Address
from .forms import AddressForm

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