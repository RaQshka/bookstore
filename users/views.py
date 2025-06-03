# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm, ProfileForm
from BookStore.models import Listing, Review, Complaint, User

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # send_mail(
            #     'Добро пожаловать!',
            #     'Спасибо за регистрацию на нашей платформе!',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [user.email],
            #     fail_silently=False,
            # )
            return redirect('users:profile')  # Используем пространство имен
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile')  # Используем пространство имен
        else:
            return render(request, 'users/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'users/login.html')

@login_required
def profile(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user
    listings = Listing.objects.filter(seller=user)
    reviews = Review.objects.filter(to_user=user)
    complaints = Complaint.objects.filter(target_user=user)
    context = {
        'user': user,
        'listings': listings,
        'reviews': reviews,
        'complaints': complaints,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Используем пространство имен
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})