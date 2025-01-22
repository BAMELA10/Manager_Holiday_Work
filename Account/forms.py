from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django import forms 

class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control col-md-12 rounded-0 fs-4',
                                   'placeholder': 'Username'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput({
                                   'class': 'form-control col-md-12 rounded-0 fs-4',
                                   'placeholder':'Password'}))