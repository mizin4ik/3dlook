from django.core.mail import mail_admins
from django.utils import timezone

from celery.utils.log import get_task_logger
from dateutil import relativedelta
from PIL import Image

from test_3dlook.celery_3dlook import app
from users.models import User

logger = get_task_logger(__name__)


@app.task(name='rotate_user_avatar')
def rotate_user_avatar(user_id):
    """Rotate user's avatar on 90 degrees."""
    try:
        user = User.objects.get(
            pk=user_id,
            avatar__isnull=False,
            is_avatar_rotated=False
        )
    except User.DoesNotExist:
        logger.error(f'User with id={user_id} was not found')
        return

    image = Image.open(user.avatar)
    rotated_image = image.transpose(Image.ROTATE_90)
    rotated_image.save(user.avatar.path)
    user.is_avatar_rotated = True
    user.save()
    logger.info(f'Avatar for user with id={user_id} successfully rotated')


@app.task(name='notify_admin_about_new_users')
def notify_admin_about_new_users():
    """Notify admin about new users via email once a day on a schedule."""
    yesterday = timezone.now() - relativedelta.relativedelta(days=1)
    new_users = User.objects.filter(date_joined__date=yesterday)

    new_users_info = ', '.join(
        (
            f'ID: {user.pk}'
            f'Username: {user.username}'
            f'Email: {user.email}'
            '\n' for user in new_users
        )
    )

    message = (
        f'New Users Count: {new_users.count()}\n'
        f'New Users Info:\n'
        f'{new_users_info}'
    )

    mail_admins(
        subject='New Users Info',
        message=message,
    )
