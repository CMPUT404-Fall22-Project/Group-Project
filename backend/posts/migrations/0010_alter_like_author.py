# Generated by Django 4.1.2 on 2022-12-05 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_like_comment_like_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='author',
            field=models.URLField(),
        ),
    ]
