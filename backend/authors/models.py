from django.db import models

class Author(models.Model):
    
    # use get_full_path to get the url and id variables
    type = "author"
    id = models.CharField(unique=True, primary_key=True, max_length=255) # e.g. '9de17f29c12e8f97bcbbd34cc908f1baba40658e'
    host = models.URLField(blank=False) # e.g. "http://127.0.0.1:5454/"
    displayName = models.CharField(max_length=255) # e.g. "Lara Croft"
    github = models.URLField() # e.g. "http://github.com/laracroft"
    profileImage = models.URLField() # e.g. "https://i.imgur.com/k7XVwpB.jpeg"

    def __str__(self):
        # set displayName as string representation of object
        return self.displayName
    
    def get_full_path(self):
        """Returns str(self.host) + "authors/" + str(self.id) """
        return str(self.host) + "authors/" + str(self.id)