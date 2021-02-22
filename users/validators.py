import logging

from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def user_avatar_validator(image):
    """
    Validation function for user's avatar.
    """
    image_size_limit = 500  # 500Kb
    print(image.size)
    if image.size > image_size_limit * 1024:
        logger.error('Validation for user avatar failed')
        raise ValidationError(f'Max size of file is {image_size_limit} KB')
