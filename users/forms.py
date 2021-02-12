from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import PasswordInput

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'form-control'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})


class LoginExistingUser(forms.Form):
    email = forms.EmailField()

    email.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        user_email = self.cleaned_data['email']
        user_email = user_email.lower()

        email_field = 'email'
        field_lookup = {f"{email_field}__iexact": user_email}
        if not get_user_model().objects.filter(**field_lookup).exists():
            raise forms.ValidationError(f'User does not exist. Try to Signup this User.')
        return user_email

