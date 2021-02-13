from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import PasswordInput

from users.models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control'})


class LoginForm(forms.Form):
    email = forms.EmailField()

    email.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        user_email = self.cleaned_data['email'].lower()

        if not get_user_model().objects.filter(email__iexact=user_email).exists():
            raise forms.ValidationError(f'User does not exist. Try to Signup this User.')
        return user_email
