from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job

User = get_user_model()


@job
def deliver_verification_email(base_url, user, token):
    subject = 'Verify your account at GameShelf'

    verification_url = f'{base_url}{token}'

    body = render_to_string(
        'users/emails/verification_email.html', {'user': user, 'verification_url': verification_url}
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


@job
def deliver_password_reset_email(base_url, user, token):
    subject = 'Reset your password'

    url = f'{base_url}{token}'

    body = render_to_string('users/emails/reset_password.html', {'user': user, 'reset_url': url})

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


@job
def deliver_activation_email(base_url, user, token):
    subject = 'Reactivate your account'

    url = f'{base_url}{token}'

    body = render_to_string('users/emails/activate_account.html', {'user': user, 'activation_url': url})

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()
