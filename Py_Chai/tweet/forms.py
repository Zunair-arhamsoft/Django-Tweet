from django import forms
from .models import Tweet, User
from django.contrib.auth.forms import UserCreationForm    

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

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        } 
        labels = {
            'username': 'Username',
            'email': 'Email Address',
        }