from django.db import models
import string
import random


def generate_random_string():
    n=32
    # e.g. 'PV8dmraVJ5hlVlTPjAix0rmO2QmTOtJ2'
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

class Author(models.Model):
    id = models.CharField(unique=True, primary_key=True, default=generate_random_string(), editable=False, max_length=255)
    type = models.CharField(max_length=255, default="author")
    host = models.URLField(blank=False) # e.g. "http://127.0.0.1:5454/"
    displayName = models.CharField(max_length=255) # e.g. "Lara Croft"
    github = models.URLField() # e.g. "http://github.com/laracroft"
    profileImage = models.URLField() # e.g. "https://i.imgur.com/k7XVwpB.jpeg"
    followers = models.ManyToManyField('self', through="Follower", symmetrical=False)
    isAuthorized = models.BooleanField(default=False) # must be manually approved by admin


    def __str__(self):
        return self.displayName
    
    def get_full_path(self):
        """Returns str(self.host) + "authors/" + str(self.id) """
        return str(self.host) + "authors/" + str(self.id)
    

class Follower(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_authors")
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_followers")

    class Meta:
        # prevent duplicate entries (still allows an entry of ('follower'),('author'))
        unique_together = (('author', 'follower'))

    def __str__(self):
        return str(self.author)