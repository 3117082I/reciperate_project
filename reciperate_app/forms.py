from django import forms
from reciperate_app import SignUp, SignIn

class SignUp(forms.ModelForm):
    username = forms.CharField(max_length= 128)