import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        """
        Method that provides preparation before testing User model's features.
        """
        self.custom_user = User.objects.create(
            pk=111,
            username='custom_user',
            password='1111',
            email='user@mail.com',
            first_name='First',
            last_name='Last',
            birthday='2021-03-01',
            is_active=True,
        )
        self.custom_user.save()

    def test_save_is_avatar_rotated_without_update_image_first_time(self):
        """
        Provide test for save method if we do not have user image
        and save changes to user account without image
        """
        custom_user = User.objects.get(id=self.custom_user.pk)
        custom_user.is_avatar_rotated = False

        custom_user.save()
        self.assertEqual(False, custom_user.is_avatar_rotated)

    def test_save_is_avatar_rotated_when_update_image(self):
        """
        Provide test for save method if we already have user image
        and try to update it.
        """
        image_path = os.path.join(
            settings.BASE_DIR, 'users/tests/images/image.png'
        )
        custom_user = User.objects.get(id=self.custom_user.pk)
        custom_user.is_avatar_rotated = True

        custom_user.avatar = SimpleUploadedFile(
            name='image.png',
            content=open(image_path, 'rb').read(),
            content_type='image/png'
        )
        custom_user.save()
        self.assertEqual(False, custom_user.is_avatar_rotated)

    def test_save_is_avatar_rotated_without_update_image(self):
        """
        Provide test for save method if we already have user image
        and save changes to user account without image .
        """
        custom_user = User.objects.get(id=self.custom_user.pk)
        custom_user.is_avatar_rotated = True
        custom_user.save()
        self.assertEqual(True, custom_user.is_avatar_rotated)

    def test_save_avatar_more_than_500_KB(self):
        """
        Provide test for save method if we try upload avatar more than 500 Kb.
        """
        image_path = os.path.join(
            settings.BASE_DIR, 'users/tests/images/bigsize_image.jpg'
        )
        custom_user = User.objects.get(id=self.custom_user.pk)

        custom_user.avatar = SimpleUploadedFile(
            name='bigsize_image.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpg'
        )
        with self.assertRaises(ValidationError) as context_manager:
            custom_user.full_clean()
        self.assertIn(
            'Max size of file is 500 KB', context_manager.exception.messages
        )
