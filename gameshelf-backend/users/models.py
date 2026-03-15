from django.conf import settings
from django.db import models
from shared.models import SoftDeleteModel

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
    
    role = models.CharField(max_length=1, choices=Role, default=Role.USER)
    