from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm, MagicForm

from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.forms import PasswordResetForm

UserModel = get_user_model()


def home(request):
    return render(request, 'users/home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'users/signup.html')
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
                'user': 'test@email.com',     # user
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # return HttpResponse('Please confirm your email address to complete the registration', message)
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
        # form = PasswordChangeForm(request.user)
        # return render(request, 'activation.html', {'form': form})

        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect(reverse_lazy(home))
    else:
        return HttpResponse('Activation link is invalid!')


def magic_send(request):
    if request.method == 'GET':
        return render(request, 'users/magic_send.html')
    if request.method == 'POST':
        form = MagicForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.set_unusable_password()
            user.authenticate()

            # Рассылка
            # current_site = get_current_site(request)    # Если несколько сайтов, то текст письма для них будет разный
            # mail_subject = 'Activate your account.'
            # message = render_to_string('users/users_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()

            return HttpResponse('Yuo are Signed In')
    else:
        form = MagicForm()
    return render(request, 'users/magic_send.html', {'form': form})


def magic_activate(request):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        # user.set_unusable_password()
        user.save()
        # return redirect('home.html')
        # https://youtu.be/kzN_VCFG9NM (37:00)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect(reverse_lazy(home))
    else:
        return HttpResponse('Activation link is invalid!')




