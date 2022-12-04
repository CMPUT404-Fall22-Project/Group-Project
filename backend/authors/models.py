from django.db import models
from django.core.exceptions import ValidationError
from utils.model_utils import generate_random_string, get_host
import uuid


class Author(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255, default="author", editable=False)
    host = models.URLField(blank=False, editable=False, default=get_host)
    displayName = models.CharField(max_length=255, null=False)
    github = models.URLField()  # e.g. "http://github.com/laracroft"
    profileImage = models.URLField(default="https://i.imgur.com/k7XVwpB.jpeg")
    isAuthorized = models.BooleanField(default=False)  # must be manually approved by admin

    def add_follower(self, follower):
        """
        Adds follower to followers of author (self)
        Raises validation error if self and follower are same author
        """
        if self.id == follower:
            raise ValidationError("Authors can't follow themselves")
        Follower(author=self, follower=follower).save()

    def __str__(self):
        return self.displayName

    def get_full_path(self):
        """Returns str(self.host) + "authors/" + str(self.id) """
        return str(self.host) + "authors/" + str(self.id)

    def authorize(self):
        """Authorizes an author by setting isAuthorized=True and then saving to db"""
        self.isAuthorized = True
        self.save()

    def is_remote(self):
        self.host != get_host()


class Follower(models.Model):

    class Meta:
        unique_together = (('author', 'follower'))

    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_authors")
    follower = models.TextField(null=False)  # the follower (could be remote!)

    # https://stackoverflow.com/questions/68811385/django-ensure-2-fields-in-a-table-of-the-same-model-type-dont-have-the-same-v
    def clean(self):
        # this check also exists in Author model. But this one is needed to handle the scenario in Django admin panel.
        if self.author.id == self.follower:
            raise ValidationError("Authors can't follow themselves")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.author)
