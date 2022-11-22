from django.db import models

class Node(models.Model):
    host = models.URLField(blank=False, editable=False)
    username = models.CharField(max_length=255)  
    password = models.CharField(max_length=255)  
    
    def __str__(self):
        return self.host