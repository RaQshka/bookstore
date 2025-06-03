from django import forms
from BookStore.models import Wishlist, Category, Tag, City

class WishlistForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox'})
    )

    class Meta:
        model = Wishlist
        fields = [
            'title', 'author', 'language', 'min_condition', 'price_min', 'price_max',
            'city', 'series', 'number_of_pages', 'isbn', 'dimensions', 'publisher',
            'cover_type', 'year', 'illustrations_type', 'description', 'is_exchange',
            'exchange_conditions', 'categories', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'min_condition': forms.Select(attrs={'class': 'form-select'}),
            'price_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'series': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_type': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'illustrations_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_exchange': forms.Select(choices=[('', 'Не важно'), (True, 'Да'), (False, 'Нет')], attrs={'class': 'form-select'}),
            'exchange_conditions': forms.Textarea(attrs={'class': 'form-control'}),
        }