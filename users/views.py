from django.shortcuts import render
# book_platform/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm, WishlistForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Исправлено для email
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'users/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

@login_required
def wishlist(request):
    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user
            wishlist_item.save()
            return redirect('wishlist')
    else:
        form = WishlistForm()
    items = WishlistForm.objects.filter(user=request.user)
    return render(request, 'users/wishlist.html', {'form': form, 'items': items})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')