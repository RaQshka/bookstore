from django import forms
from BookStore.models import Listing, Category, Tag


class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox'}),
        required=False,
        label="Теги"
    )
    image = forms.ImageField(required=False, label="Изображение")

    class Meta:
        model = Listing
        fields = [
            'title', 'author', 'series', 'number_of_pages', 'isbn', 'dimensions',
            'publisher', 'cover_type', 'year', 'illustrations_type', 'language',
            'description', 'category', 'price', 'is_exchange', 'condition',
            'exchange_conditions', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'series': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_type': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'illustrations_type': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_exchange': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'exchange_conditions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }