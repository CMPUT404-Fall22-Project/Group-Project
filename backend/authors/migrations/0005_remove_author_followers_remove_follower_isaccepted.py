# Generated by Django 4.1.2 on 2022-11-23 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0004_alter_follower_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='isAccepted',
        ),
    ]