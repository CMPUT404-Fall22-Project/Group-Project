# Generated by Django 4.1.2 on 2022-11-28 05:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_alter_author_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='follower',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]
