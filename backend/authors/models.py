from django.db import models

class Author(models.Model):
    
    type = "author"
    id = models.CharField(unique=True, primary_key=True, max_length=255) # e.g. '9de17f29c12e8f97bcbbd34cc908f1baba40658e'
    host = models.URLField(blank=False) # e.g. "http://127.0.0.1:5454/"
    displayName = models.CharField(max_length=255) # e.g. "Lara Croft"
    url = str(host) + "authors/" + str(id) # e.g. "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e"
    github = models.URLField() # e.g. "http://github.com/laracroft"
    profileImage = models.URLField() # e.g. "https://i.imgur.com/k7XVwpB.jpeg"

    def __str__(self):
        # set displayName as string representation of object
        return self.displayName