from django import forms
from BookStore.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # От 1 до 5 звезд
            'text': forms.Textarea(attrs={'rows': 4}),
        }