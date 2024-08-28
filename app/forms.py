
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from news_website import settings

class RegisterUserForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.

    Наследует от UserCreationForm и добавляет дополнительные поля для логина, адреса электронной почты, пароля и подтверждения пароля. Поля настроены с пользовательскими классами CSS для улучшения внешнего вида.

    :param username: Поле для ввода логина пользователя.
    :param email: Поле для ввода адреса электронной почты.
    :param password1: Поле для ввода пароля.
    :param password2: Поле для подтверждения пароля.
    """
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input form-control'}))
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'form-input form-control'}), input_formats=settings.DATE_INPUT_FORMATS)
    bio = forms.CharField(label='О себе', widget=forms.Textarea(attrs={'class': 'form-input form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        profile = Profile(
            user=user,
            full_name=self.cleaned_data['full_name'],
            email=self.cleaned_data['email'],
            birth_date=self.cleaned_data['birth_date'],
            bio=self.cleaned_data['bio']
        )
        if commit:
            user.save()
            profile.save()
        return user

class LoginUserForm(AuthenticationForm):
    """
    Форма для входа пользователя в систему.

    Наследует от AuthenticationForm и добавляет поля для логина и пароля с пользовательскими классами CSS. Предоставляет функционал для аутентификации пользователя.

    :param username: Поле для ввода логина пользователя.
    :param password: Поле для ввода пароля пользователя.
    """
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))