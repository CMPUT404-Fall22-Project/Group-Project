from django.db import models
from django.utils import timezone
from utils.model_utils import generate_random_string
from authors.models import Author


# Create your models here.
class Post(models.Model):

    class ContentType(models.TextChoices):
        # for HTML you will want to strip tags before displaying
        TEXT_MARKDOWN = "text/markdown" # common mark
        TEXT_PLAIN = "text/plain" # UTF-8
        APPLICATION = "application/base64"
        PNG = "image/png;base64" # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
        JPEG = "image/jpeg;base64" # this is an embedded jpeg

    type = models.CharField(max_length=255, default="post", editable=False)
    id = models.CharField(primary_key=True, editable=False, max_length=255, default=generate_random_string)
    title = models.CharField(max_length=255, null=False)
    source = models.URLField(null=False)
    origin = models.URLField(null=False)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # The content type of the post
    # assume either
    # text/markdown -- common mark
    # text/plain -- UTF-8
    # application/base64
    # image/png;base64 # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
    # image/jpeg;base64 # this is an embedded jpeg
    # for HTML you will want to strip tags before displaying
    contentType = models.CharField(choices = ContentType.choices, null=False)
    count = models.IntegerField(default=0)
    published = models.DateTimeField(default=timezone.now, blank=False)


class Category(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category =  models.CharField(max_length=255) # TODO: Do we know what all of the potential categories are?

    class Meta:
        # eliminate duplicate categories for a post
        unique_together = (('post', 'category'))