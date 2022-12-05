from rest_framework import serializers
from .models import Post, Comment, Like
from authors.models import Author
from authors.serializers import AuthorSerializer
from django.shortcuts import get_object_or_404


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["context","type","object","author"]


class LikeSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField()
    # summary = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ["context","type","object","author"]

    # def get_author(self, obj: Like):
    #     author = AuthorSerializer(obj.author).data       
    #     return author

    # def get_summary(self, obj: Like):
    #     return f"{obj.author.displayName} Likes your post"