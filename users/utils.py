from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_email(request, form, user):
    # Send an email to user with token:
    mail_subject = 'Activate your account.'
    current_site = get_current_site(request)
    message = render_to_string('users/users_active_email.html', {
        'user': user.email,  # user
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
