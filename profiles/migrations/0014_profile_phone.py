# Generated by Django 4.1.3 on 2023-01-01 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_alter_profile_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]
