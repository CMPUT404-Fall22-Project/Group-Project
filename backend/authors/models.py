from django.db import models
from django.core.exceptions import ValidationError
import random
import string

def get_scheme_and_netloc():
    """TODO: This needs to include scheme and netloc"""
    return 'http://127.0.0.1:8000/'

def generate_random_string():
    # e.g. 'PV8dmraVJ5hlVlTPjAix0rmO2QmTOtJ2'
    n=32
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class Author(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255, default=generate_random_string)
    type = models.CharField(max_length=255, default="author", editable=False)
    host = models.URLField(blank=False, editable=False, default=get_scheme_and_netloc)
    displayName = models.CharField(max_length=255, null=False)
    github = models.URLField() # e.g. "http://github.com/laracroft"
    profileImage = models.URLField() # e.g. "https://i.imgur.com/k7XVwpB.jpeg"
    followers = models.ManyToManyField('self', through="Follower", symmetrical=False)
    isAuthorized = models.BooleanField(default=False) # must be manually approved by admin

    def add_follower(self, follower):
        """
        Adds follower to followers of author (self)
        Raises validation error if self and follower are same author
        """
        if self == follower:
            raise ValidationError("Authors can't follow themselves")
        self.followers.add(follower) # this adds to the Follower table

    def __str__(self):
        return self.displayName
    
    def get_full_path(self):
        """Returns str(self.host) + "authors/" + str(self.id) """
        return str(self.host) + "authors/" + str(self.id)
        

class Follower(models.Model):

    class Meta:
        unique_together = (('author', 'follower'))

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_authors")
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_followers")
    isAccepted = models.BooleanField(default=False) # must be approved by author

    # https://stackoverflow.com/questions/68811385/django-ensure-2-fields-in-a-table-of-the-same-model-type-dont-have-the-same-v
    def clean(self):
        if self.author == self.follower: # this check also exists in Author model. But this one is needed to handle the scenario in Django admin panel.
            raise ValidationError("Authors can't follow themselves")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.author)