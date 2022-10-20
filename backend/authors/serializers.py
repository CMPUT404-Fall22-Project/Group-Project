from rest_framework import serializers

from .models import Author, Follower


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # TODO: Bug when fields isn't set to "__all__":
        # `HyperlinkedIdentityField` requires the request in the serializer context.
        # Add `context={'request': request}` when instantiating the serializer.
        # fields = ["type", "id", "host", "displayName", "url", "github", "profileImage"]
        fields = "__all__"

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"