from django import forms
from .models import Recipe
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        field = ('username', 'password')

class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput()



class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'url', 'category', 'image']