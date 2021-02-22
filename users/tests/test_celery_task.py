import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from test_3dlook import celery_3dlook
from users.models import User
from users.tasks import notify_admin_about_new_users, rotate_user_avatar


class CeleryTasksTestCase(TestCase):
    def setUp(self):
        """
        Method that provides preparation before testing Celery tasks.
        """
        celery_3dlook.app.conf['task_always_eager'] = True

        image_path = os.path.join(
            settings.BASE_DIR, 'users/tests/images/image.png'
        )
        self.custom_user = User.objects.create(
            pk=111,
            avatar=SimpleUploadedFile(
                name='image.png',
                content=open(image_path, 'rb').read(),
                content_type='image/png'
            ),
        )
        self.custom_user.save()

    def test_rotate_user_avatar_success(self):
        """
        Provide tests for `rotate_user_avatar` task.
        """
        task = rotate_user_avatar.s(
            user_id=self.custom_user.pk
        ).delay()
        task.get()
        self.assertEqual(task.status, 'SUCCESS')

    def notify_admin_about_new_users_success(self):
        """
        Provide tests for `notify_admin_about_new_users` task.
        """
        task = notify_admin_about_new_users().delay()
        task.get()
        self.assertEqual(task.status, 'SUCCESS')
