from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.utils.translation import override
from django_rq import job
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()

@job
def deliver_new_games_notification(base_url, games):

    active_profiles = Profile.objects.select_related('user').iterator()
    
    subject = _('New games are here!')

    body = render_to_string(
        'games/emails/new_games.html', {'base_url': base_url, 'games': games}
    )
    
    for profile in active_profiles: 
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[profile.user.email],
        )
        email.content_subtype = 'html'
        email.send()
