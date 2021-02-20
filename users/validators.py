from django.core.exceptions import ValidationError


def user_avatar_validator(image):
    image_size_limit = 500  # 500Kb
    print(image.size)
    if image.size > image_size_limit * 1024:
        raise ValidationError(f'Max size of file is {image_size_limit} KB')
