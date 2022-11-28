# Generated by Django 4.1.2 on 2022-11-28 06:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_rename_visibilty_post_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]