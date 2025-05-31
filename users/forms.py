# book_platform/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Wishlist

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'avatar_url', 'description', 'city']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['book_title', 'author']