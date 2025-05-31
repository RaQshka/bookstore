# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from BookStore.models import User, Wishlist, City

class RegistrationForm(UserCreationForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Выберите город")

    class Meta:
        model = User
        fields = ['email', 'username', 'city', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'avatar_url', 'description', 'city']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['title', 'author']