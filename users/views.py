from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.db.models import F
from django.views.generic.base import TemplateView

from .forms import LoginForm, SignupForm
from .utils import send_email

UserModel = get_user_model()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'
    login_url = '/home/'


def magic_login(request):
    if request.method == 'GET':
        form = LoginForm()
        users = UserModel.objects.all()
        return render(request, 'users/magic_login.html', context={'form': form, 'users': users})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Get existing user from DB:
            user_email = form.cleaned_data.get('email')
            user = get_user_model().objects.get(email=user_email)
            user.is_active = False
            # user.save()

            # Counter
            user.views = F('views') + 1
            user.save()
            user.refresh_from_db()

            # Send email to user with token:
            send_email(request, form, user)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = LoginForm()

    users = UserModel.objects.all()
    return render(request, 'users/magic_login.html', context={'form': form, 'users': users})


def magic_signup(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'users/magic_signup.html', {'form': form})
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            # user.save()

            # Counter
            user.views = 1
            user.save()
            user.refresh_from_db()

            # Send email to user with token:
            send_email(request, form, user)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'users/magic_signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # Activate user and login:
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        return HttpResponse('Activation link is invalid!')
