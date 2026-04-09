import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from django_rq import job

from games.models import Game, Review

@job
def deliver_games_notification(base_url, user):
    # file_dir = os.path.join(settings.BASE_DIR, 'media', 'notifications', 'games')
    # os.makedirs(file_dir, exist_ok=True)

    # filepath = generate_games_notification(file_dir, user)

    body = render_to_string(
        'subjects/emails/certificate.html',
        {
            'user': user,
            'base_url': base_url,
        }
    )

    email = EmailMessage(
        subject='',
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()

