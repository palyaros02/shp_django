
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings

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
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'form-input form-control', 'type': 'date'}), input_formats=settings.DATE_INPUT_FORMATS)
    bio = forms.CharField(label='О себе', widget=forms.Textarea(attrs={'class': 'form-input form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
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

class ProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.

    Наследует от ModelForm и добавляет поля для редактирования полного имени, даты рождения, адреса электронной почты, биографии и аватара пользователя. Поля настроены с пользовательскими классами CSS для улучшения внешнего вида.
    """
    class Meta:
        model = Profile
        fields = ['full_name', 'birth_date', 'email', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'label': 'Полное имя'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Дата рождения'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'О себе'}),
        }

class EditUserProfileForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form-input form-control'}))
    password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}), required=False)
    password2 = forms.CharField(label='Подтвердите новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}), required=False)
    full_name = forms.CharField(label='ФИО', required=False, widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    birth_date = forms.DateField(label='Дата рождения', required=False, widget=forms.DateInput(attrs={'class': 'form-input form-control', 'type': 'date'}), input_formats=settings.DATE_INPUT_FORMATS)
    bio = forms.CharField(label='О себе', required=False, widget=forms.Textarea(attrs={'class': 'form-input form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']
        profile = Profile.objects.get(user=user)
        super().__init__(*args, **kwargs)
        self.fields['full_name'].initial = profile.full_name
        self.fields['birth_date'].initial = profile.birth_date.strftime('%Y-%m-%d')
        self.fields['bio'].initial = profile.bio

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            profile.full_name = self.cleaned_data['full_name']
            profile.birth_date = self.cleaned_data['birth_date']
            profile.bio = self.cleaned_data['bio']
            profile.save()
        return user