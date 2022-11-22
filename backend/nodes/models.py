from django.db import models

# Create your models here.

class Node(models.Model):
    host = models.URLField(blank=False, editable=False)