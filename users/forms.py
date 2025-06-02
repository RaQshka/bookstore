# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from BookStore.models import User, City, Wishlist

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    patronymic = forms.CharField(max_length=30, required=False, label="Отчество")
    phone_number = forms.CharField(max_length=15, required=False, label="Номер телефона")
    email = forms.EmailField(required=True, label="Почта")
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=True, label="Город")
    username = forms.CharField(max_length=150, required=True, label="Логин")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'city', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Этот логин уже занят.")
        return username

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'city', 'avatar', 'description']
        widgets = {'avatar': forms.FileInput()}