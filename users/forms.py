# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from BookStore.models import User, City, Wishlist
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}), required=True, label="Имя")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'}), required=True, label="Фамилия")
    patronymic = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше отчество'}), required=False, label="Отчество")
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш номер телефона'}), required=False, label="Номер телефона")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу почту'}), required=True, label="Почта")
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), required=True, label="Город")
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш логин'}), required=True, label="Логин")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}), label="Подтверждение пароля")

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