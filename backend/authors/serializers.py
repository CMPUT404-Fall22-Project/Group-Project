from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # don't include followers or isAuthorized
        fields = ["id","type","host","displayName","github","profileImage"]