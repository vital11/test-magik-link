from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm, LoginExistingUser


UserModel = get_user_model()


def home(request):
    return render(request, 'users/home.html')


# LOGIN
def login_existing_user(request):
    if request.method == 'GET':
        form = LoginExistingUser()
        return render(request, 'users/login_existing_user.html', {'form': form})
    if request.method == 'POST':
        form = LoginExistingUser(request.POST)
        if form.is_valid():
            # Get existing user from DB:
            user_email = form.cleaned_data.get('email')

            # # Проверка email на exists() в БД во вьюхе:
            # user_exist = get_user_model().objects.filter(email=user_email).exists()
            # if user_exist:
            #     user = get_user_model().objects.get(email=user_email)
            #     user.is_active = False
            #     user.save()
            # else:
            #     return HttpResponse('Пользователь с таким email не существует.')

            user = get_user_model().objects.get(email=user_email)
            user.is_active = False
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('users/users_active_email.html', {
                'user': user.email,     # user
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = LoginExistingUser()
    return render(request, 'users/login_existing_user.html', {'form': form})


def activate_existing_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # activate user and login:
        user.is_active = True
        user.save()
        login(request, user)
        # form = PasswordChangeForm(request.user)
        # return render(request, 'activation.html', {'form': form})

        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect(reverse_lazy(home))
    else:
        return HttpResponse('Activation link is invalid!')


# SIGNUP
def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('users/users_active_email.html', {
                'user': user.email,     # user
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # activate user and login:
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse_lazy(home))
    else:
        return HttpResponse('Activation link is invalid!')

