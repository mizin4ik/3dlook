from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.validators import user_avatar_validator


class User(AbstractUser):
    avatar = models.ImageField(
        verbose_name=_('avatar'),
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=(user_avatar_validator,)
    )

    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('birthday')
    )
    is_avatar_rotated = models.BooleanField(default=False)

    __original_avatar = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_avatar = self.avatar

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.avatar != self.__original_avatar:
            self.is_avatar_rotated = False
        super().save(force_insert, force_update,  *args, **kwargs)
        self.__original_avatar = self.avatar
