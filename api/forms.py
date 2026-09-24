"""
Forms for user registration and authentication.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomRegistrationForm(UserCreationForm):
    """
    Custom user registration form extending Django's UserCreationForm
    
    Defines custom fields and widgets for user registration.
    """
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': "form-control mb-2 p-1 mb-2",
        'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': "form-control mb-2 p-1 mb-2",
        'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': "form-control mb-2 p-1 mb-2",'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': "form-control mb-2 p-1 mb-2"}))
    #dob = forms.DateField(required=True, widget=forms.DateInput(attrs={
    #    'class': "form-control mb-2 p-1 mb-2",
    #    'type': 'date', 'placeholder': 'Date of Birth'}))
    password1 = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={
        'class': "form-control mb-2 p-1 mb-2"}))
    password2 = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput(attrs={
        'class': "form-control mb-2 p-1 mb-2"}))
    #profile_image = forms.ImageField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "dob", "profile_image")

class CustomLoginForm(AuthenticationForm):
    """
    Custom user login form extending Django's AuthenticationForm
    
    Defines custom fields and widgets for user login.
    """
    
    username = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class': "form-control mb-2 p-1 mb-2", 'placeholder': 'Email'}))
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(
        attrs={'class': "form-control mb-2 p-1", 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ("username", "password")
    
    def confirm_login_allowed(self, user):
        #Allows users to login regardless of whether they are active or not
        pass