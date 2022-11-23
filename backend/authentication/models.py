from django.db import models

from authors.models import Author


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=255, null=False)
    passwordHash = models.CharField(max_length=255, null=False)
    salt = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)  # shorthand for faster access
    token = models.CharField(primary_key=True, max_length=64, null=False)


class ExternalNode(models.Model):
    url = models.CharField(primary_key=True, max_length=255, null=False)
    authorization = models.CharField(max_length=255, null=False)
