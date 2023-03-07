from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *


class CreateUserForm(UserCreationForm):
    '''Форма для регистрации пользователя на сайт.'''
    
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','email']
        
class UserLogin(AuthenticationForm):
    '''Форма для входа пользователя на сайт.'''
    
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UserUpdateForm(forms.ModelForm):
    '''Форма для обновления данных пользователя.'''
    
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email']
 
 
class ProfileUpdateForm(forms.ModelForm):
    '''Форма для обновление аватара пользователя.'''
    
    class Meta:
        model = Profile
        fields = ['image']
    