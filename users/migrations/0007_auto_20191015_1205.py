# Generated by Django 2.2.5 on 2019-10-15 06:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_auto_20191015_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='follower_by',
        ),
        migrations.AddField(
            model_name='follower',
            name='followed_by',
            field=models.ManyToManyField(related_name='_follower_followed_by_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
