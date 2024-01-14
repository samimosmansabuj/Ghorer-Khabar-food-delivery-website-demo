from django import forms
from .models import Custom_User
from django.contrib.auth.forms import UserCreationForm

class User_Create_Form(forms.ModelForm):
    USER_TYPE = [
            ('Normal User', 'Normal User'),
            ('Merchant', 'Merchant'),
        ]
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputUsername'
    }))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'id': 'inputEmail'
    }))
    phone_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPhoneNumber'
    }))
    user_type = forms.CharField(max_length=50, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputUserType'}, choices=USER_TYPE))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'inputPassword'
    }))
    
    class Meta:
        model = Custom_User
        fields = ['username', 'email', 'phone_number', 'user_type', 'password']


class Login_Form(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputUsername'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'inputPassword'
    }))

