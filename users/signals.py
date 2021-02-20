from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from users.tasks import rotate_user_avatar


@receiver(post_save, sender=User)
def rotate_avatar(instance, **kwargs):
    # Rotate avatar if not rotated
    if instance.avatar and not instance.is_avatar_rotated:
        rotate_user_avatar.apply_async(kwargs={'user_id': instance.pk})
