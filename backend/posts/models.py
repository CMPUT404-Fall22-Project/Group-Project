from django.db import models
from django.utils import timezone
from utils.model_utils import generate_random_string
from authors.models import Author
from django.utils.translation import gettext_lazy as _
import uuid


class ContentType(models.TextChoices):
    # for HTML you will want to strip tags before displaying
    TEXT_MARKDOWN = "text/markdown", _("markdown")  # common mark
    TEXT_PLAIN = "text/plain", _("text/plain")  # UTF-8
    APPLICATION = "application/base64", _("application")
    # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
    PNG = "image/png;base64", _("png")
    JPEG = "image/jpeg;base64", ("jpeg")  # this is an embedded jpeg


class Post(models.Model):

    class Visibility(models.TextChoices):
        PUBLIC = 'PUBLIC', _("Public")
        FRIENDS = 'FRIENDS', _("Friends")
        PRIVATE = 'PRIVATE', _("Private")

    type = models.CharField(max_length=4, default="post", editable=False)
    title = models.CharField(max_length=255, null=False)
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    contentType = models.CharField(choices=ContentType.choices, null=False,
                                   max_length=255, default=ContentType.TEXT_PLAIN)
    content = models.TextField(null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # categories (see Models below)
    # count (total number of comments)
    # comments (see Models below)
    # commentsSrc is OPTIONAL and can be missing
    # You should return ~ 5 comments per post.
    # should be sorted newest(first) to oldest(last)
    # this is to reduce API call counts
    published = models.DateTimeField(default=timezone.now, blank=False)
    visibility = models.CharField(choices=Visibility.choices, max_length=7, default=Visibility.PUBLIC)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):

    category = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('category', 'post'))


class Comment(models.Model):

    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=7, default="comment", editable=False)
    # the author that commented
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
    # the Post that was commented on
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    contentType = models.CharField(choices=ContentType.choices, null=False,
                                   max_length=255, default=ContentType.TEXT_PLAIN)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now, blank=False)


class Like(models.Model):

    context = models.URLField()
    # summary (let serializer do it)
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=4, default="like", editable=False)
    # the author that clicked 'like'
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True)
    # the Post or Comment that liked this
    object = models.URLField()
