from django.db import models
from backend.utils.model_utils import generate_random_string

# Create your models here.
class Post(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255, default=generate_random_string)