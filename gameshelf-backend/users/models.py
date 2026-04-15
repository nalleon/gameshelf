from django.conf import settings
from django.db import models
from shared.models import SoftDeleteModel
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from colorfield.fields import ColorField
class Profile(SoftDeleteModel):
    class Role(models.TextChoices):
        USER = 'U', 'User'
        ADMIN = 'A', 'Admin'

    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png', null=True, blank=True)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )
    
    color_bg = ColorField(default='#79A998')
    role = models.CharField(max_length=1, choices=Role, default=Role.USER)
    

class UserToken(models.Model):
    class TokenType(models.TextChoices):
        VERIFY_EMAIL = 'VERIFY_EMAIL'
        CHANGE_PASSWORD = 'CHANGE_PASSWORD'
        ACTIVATE_ACCOUNT = 'ACTIVATE_ACCOUNT'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    type = models.CharField(max_length=32, choices=TokenType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at