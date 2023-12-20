from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from tinymce.widgets import TinyMCE



class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name","last_name","email")

class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("image", "description")

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['title', 'content']
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body']

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']