# Generated by Django 4.1 on 2022-08-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_comments_table_alter_posts_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='like_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
