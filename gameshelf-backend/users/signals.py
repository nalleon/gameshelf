from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from game_collections.models import Wishlist  
from libraries.models import Library


@receiver(post_save, sender=Profile)
def create_profile_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.get_or_create(user=instance.user)
        
@receiver(post_save, sender=Profile)
def create_user_library(sender, instance, created, **kwargs):
    if created:
        Library.objects.create(user=instance.user)