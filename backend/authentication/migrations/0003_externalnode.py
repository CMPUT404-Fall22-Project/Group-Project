# Generated by Django 4.1.2 on 2022-11-23 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_session_expiresat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalNode',
            fields=[
                ('url', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('authorization', models.CharField(max_length=255)),
            ],
        ),
    ]