from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        # Automatically create profile
        Profile.objects.create(user=user)

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")

            # Check if the user is staff/admin
            if user.is_staff:  
                # Redirect to custom dashboard
                return redirect('dashboard_home')  # replace with your dashboard URL name
            else:
                # Redirect normal users
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("index")


        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')
        

@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Update User
        user = request.user
        user.username = username
        user.email = email
        user.save()

        # Update Profile
        profile = user.profile
        profile.phone = phone
        profile.address = address
        profile.city = city
        profile.state = state
        profile.pincode = pincode
        profile.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile')

    return render(request, 'accounts/profile.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('index')
