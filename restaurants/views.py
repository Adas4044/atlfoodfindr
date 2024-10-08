from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import EditProfileForm, SecurityQuestionForm, CustomUserCreationForm
from .models import Favorite, UserProfile
from django.contrib.auth.models import User
from django.http import FileResponse
import os
from django.conf import settings

#favicon
def favicon_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'favicon.jpg')
    return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')

# Landing Page
def landing_page(request):
    return render(request, 'restaurants/landing_page.html')

def get_favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        favorite_ids = [favorite.place_id for favorite in favorites]
        return JsonResponse({'favorites': favorite_ids})
    return JsonResponse({'favorites': []})

# Login Page
def login_page(request):
    return render(request, 'restaurants/login_page.html')

# Signup Page
def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'restaurants/signup_page.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'restaurants/signup_page.html', {'form': form})

# Profile Page
@login_required
def profile_page(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'restaurants/profile_page.html', {'favorites': favorites})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("Posted: username = ", username, " password = ", password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("You are logged in")
            # Redirect to the landing page (use '/' or the name of your home route)
            return redirect('landing_page')  # Redirect to landing page
        else:
            print("Invalid username or password")
            return render(request, "restaurants/login_page.html", {'error': 'Invalid credentials'})
    return render(request, 'restaurants/login_page.html')

def user_logout(request):
    logout(request)
    # Redirect to the landing page after logout
    return redirect('landing_page')  # Redirect to landing page


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_page')  # Redirect to profile page after updating
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'restaurants/edit_profile.html', {'form': form})

@login_required
def add_favorite(request, place_id, name, address):
    if not Favorite.objects.filter(user=request.user, place_id=place_id).exists():
        Favorite.objects.create(user=request.user, restaurant_name=name, restaurant_address=address, place_id=place_id)
    return JsonResponse({'success': True})

@login_required
def remove_favorite(request, place_id):
    Favorite.objects.filter(user=request.user, place_id=place_id).delete()
    return redirect('profile_page')

@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'restaurants/profile_page.html', {'favorites': favorites})


def password_reset_view(request):
    if request.method == 'POST':
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            answer_1 = form.cleaned_data['answer_1']
            answer_2 = form.cleaned_data['answer_2']
            answer_3 = form.cleaned_data['answer_3']
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(username=username)

                # Check if the email matches the email linked to the username
                if user.email != email:
                    messages.error(request, 'Email does not match our records for this username.')
                else:
                    try:
                        user_profile = UserProfile.objects.get(user=user)

                        if (user_profile.security_answer_1 == answer_1 and
                            user_profile.security_answer_2 == answer_2 and
                            user_profile.security_answer_3 == answer_3):
                            # If all security answers match, reset the password
                            user.password = make_password(new_password)
                            user.save()
                            messages.success(request, 'Your password has been reset successfully.')
                            return redirect('login')
                        else:
                            messages.error(request, 'Security answers do not match.')
                    except UserProfile.DoesNotExist:
                        messages.error(request, 'Security questions not set up for this user.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Invalid form input.')
    else:
        form = SecurityQuestionForm()

    return render(request, 'restaurants/password_reset.html', {'form': form})