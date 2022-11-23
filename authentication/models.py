from django.db import models

from authors.models import Author
import time

TOKEN_EXPIRY_DELAY = 60 * 60 * 24  # one day


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=255, null=False)
    passwordHash = models.CharField(max_length=255, null=False)
    salt = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)  # shorthand for faster access
    token = models.CharField(primary_key=True, max_length=64, null=False)
    expiresAt = models.BigIntegerField(null=False)

    def _get_current_time(self):
        return int(time.time())

    def _get_new_expiry_time(self):
        return self._get_current_time() + TOKEN_EXPIRY_DELAY

    def regenerate_expiry(self):
        self.expiresAt = self._get_new_expiry_time()
        self.save()

    def is_expired(self):
        return self._get_current_time() > self.expiresAt
