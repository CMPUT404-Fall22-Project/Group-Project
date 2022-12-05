from rest_framework import serializers
from .models import Post, Comment, CommentLike, PostLike
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


class PostLikeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = ["context","type","object","author","summary"]

    def get_author(self, obj: PostLike):
        author = AuthorSerializer(obj.author).data       
        return author

    def get_summary(self, obj: PostLike):
        return f"{obj.author.displayName} Likes your post"


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"