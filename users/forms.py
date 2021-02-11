from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm

from users.models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username')


# Для админки
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class MagicForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class LoginForm(ModelForm):
    pass
