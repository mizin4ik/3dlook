# Generated by Django 2.2 on 2021-02-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210219_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_avatar_rotated',
            field=models.BooleanField(default=False),
        ),
    ]
