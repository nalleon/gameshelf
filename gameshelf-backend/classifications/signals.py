from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Classification

@receiver(pre_save, sender=Classification)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        slug = base_slug
    
        counter = 1
        Model = sender

        while Model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        instance.slug = slug