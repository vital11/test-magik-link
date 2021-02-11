from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'views', 'is_staff', 'is_active', 'password', ]
    list_display_links = ['email']
    list_editable = ('is_active', 'is_staff',)


admin.site.register(CustomUser, CustomUserAdmin)
