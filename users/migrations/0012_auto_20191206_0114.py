# Generated by Django 2.2.5 on 2019-12-05 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20191128_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio_for_profile',
            field=models.TextField(blank=True),
        ),
    ]
