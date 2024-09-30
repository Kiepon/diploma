from datetime import datetime
from django.contrib.auth.models import User
from django import forms
from . import validators
import re

class UserRegistrationForm(forms.ModelForm):
    
    username = forms.CharField(
        label='Имя:',
        max_length=150,
        help_text=(
            ""
        ),
        error_messages={
            "unique": ("Пользователь с таким именем уже существует."),
        },
    )
    email = forms.EmailField(
        label='Почта:', 
        required=True,
        error_messages={
            "unique": ("Пользователь с такой почтой уже существует.")
        },
    )
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован")
    
    class Meta:
        model = User
        fields = ('username', 'email',)
    
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']
    
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Имя:',
        max_length=150,
        required=True
    )
    password = forms.CharField(label="Пароль:", required=True, widget=forms.PasswordInput)
    
class SelectCityHotelForm(forms.Form): 
    city = forms.CharField(
    max_length=255,
    required=True,
    label='',
    widget=forms.TextInput(attrs={'class': 'city', 'placeholder': 'Выберите город', 'class': 'form-control'}),
    )
    
    check_in_date = forms.CharField(
    required=True, 
    label='',
    widget=forms.TextInput(attrs={'id': 'checkIn', 'placeholder': 'Заезд — Выезд', 'class': 'form-control bg-white', 'readOnly': 'true'}),
    )
    
    adults_childs_count = forms.CharField(
    required=False, 
    label='',
    widget=forms.TextInput(attrs={'id': 'adults-childs-count', 'readOnly': 'true', 'value': '2 взрослых', 
                                'class': 'form-control bg-white adults_childs'})
    )
    
    
    