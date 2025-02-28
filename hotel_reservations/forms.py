from django.contrib.auth.models import User
from django import forms
from . import validators
from django.core.validators import EmailValidator
from hotel_reservations.models import Subscribe
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

class UserRegistrationForm(forms.ModelForm):
    
    username = forms.CharField(
        max_length=150,
        help_text=(
            ""
        ),
        error_messages={
            "unique": ("Пользователь с таким именем уже существует."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите Ваше имя'}),
    )
    email = forms.EmailField( 
        required=True,
        error_messages={
            "unique": ("Пользователь с такой почтой уже существует.")
        },
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите почту'})
    )
    password = forms.CharField(
        label='Пароль:',                               
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Повторите пароль:',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Повторите пароль'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже зарегистрирован")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован")
        return email
    
    class Meta:
        model = User
        fields = ('username', 'email',)
    
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
    
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Имя:',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите имя или почту'}),
    )
    password = forms.CharField(
    label="Пароль:",
    required=True, 
    widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'})
    )
    
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
    

class SubscribeForm(ModelForm):

    subscribe = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите почту',
            }
        )
    )
    class Meta:
        model = Subscribe
        fields = ['subscribe',]
        error_messages = {
            'invalid': 'Пользователь с такой почтой уже существует.'
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': "Имя:",
            'email': "Почта",
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-inline mb-4 form-control', 
                'placeholder': 'Введите имя',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-inline mb-4 form-control', 
                'placeholder': 'Введите почту'
            })
        }
        
class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        
        self.fields['new_password1'].help_text = ''
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-inline mb-4 form-control',
            'placeholder': 'Введите старый пароль',
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-inline mb-4 form-control',
            'placeholder': 'Введите новый пароль',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-inline mb-4 form-control',
            'placeholder': 'Подтвердите пароль',
        })
        self.fields['old_password'].error_messages = {
            'required': ('Старый пароль обязателен.'),
            'invalid': ('Старый пароль неверен.'),
        }
        self.fields['new_password1'].error_messages = {
            'required': ('Новый пароль обязателен.'),
            'too_short': ('Пароль слишком короткий.'),
            'too_common': ('Пароль слишком распространённый.'),
            'invalid': ('Пароль не соответствует требованиям.'),
        }
        self.fields['new_password2'].error_messages = {
            'required': ('Подтверждение пароля обязательно.'),
            'mismatch': ('Пароли не совпадают.'),
        }
        
    def clean(self):
        super().clean()
        errors = self._errors
        if errors:
            first_error = next(iter(errors.values()), None)
            if first_error:
                for field in list(errors.keys()):
                    if errors[field] != first_error:
                        del errors[field]
        return self.cleaned_data
    


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-reset-pass', 'placeholder': 'Введите почту', "autocomplete": "email"}
        )
    )
    
class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадают"
    }
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите новый пароль',
                'autocomplete': 'new-password',
            }
        ),
        strip=False,
    )
    
    new_password2 = forms.CharField(
        strip=False,
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Подтвердите новый пароль',
                'autocomplete': 'new-password',
            
            }
        )
    )