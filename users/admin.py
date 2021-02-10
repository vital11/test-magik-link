from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = CustomUser
    list_display = ['username', 'email', 'views', 'is_staff', 'is_active', ]
    list_display_links = ['username', 'email']
    list_editable = ('is_active', )


admin.site.register(CustomUser, CustomUserAdmin)
