from django import forms
from .models import Tweet     

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'What\'s happening?'}),
            'photo': forms.ClearableFileInput(attrs={'multiple': False}),
        }
        labels = {
            'text': 'Tweet',
            'photo': 'Add Photo (optional)',
        }