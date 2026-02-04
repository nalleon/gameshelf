import uuid

from django.conf import settings
from django.db import models

class Profile(models.Model):
    class Role(models.TextChoices):
        USER = 'User'
        ADMIN = 'Admin'

    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png', null=True, blank=True)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )
    
    role = models.CharField(max_length=1, choices=Role, default=Role.USER)
    
class Token(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)
