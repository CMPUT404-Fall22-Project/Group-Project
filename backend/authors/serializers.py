from rest_framework import serializers

from .models import Author, Follower


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class AuthorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["host", "displayName", "github", "profileImage"]



class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"