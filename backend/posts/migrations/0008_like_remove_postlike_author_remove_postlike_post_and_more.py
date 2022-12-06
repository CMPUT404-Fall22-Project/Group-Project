# Generated by Django 4.1.2 on 2022-12-05 14:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_alter_author_id_alter_follower_id_and_more'),
        ('posts', '0007_alter_comment_id_alter_commentlike_id_alter_post_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('context', models.URLField()),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(default='like', editable=False, max_length=4)),
                ('object', models.URLField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='authors.author')),
            ],
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='post',
        ),
        migrations.DeleteModel(
            name='CommentLike',
        ),
        migrations.DeleteModel(
            name='PostLike',
        ),
    ]
