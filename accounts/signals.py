from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile
import random, string

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,**kwargs):
    if created:
        dummy_username = ''.join(random.choices(string.ascii_letters, k=30))
        Profile.objects.create(user=instance, username=dummy_username)
    else:
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("save_user_profile")
    instance.profile.save()
