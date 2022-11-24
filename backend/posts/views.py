from django.shortcuts import get_object_or_404
from utils.model_utils import generate_random_string
from utils.requests import paginate
from utils.process_models import process_posts, serialize_single_post
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.http import HttpResponse
from authors.models import Author
from .models import ContentType, Post, Comment, PostLike, CommentLike, Category
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from authors.serializers import AuthorSerializer
from inbox.views import send_to_all_followers
import base64

# Be aware that Posts can be images that need base64 decoding.
# posts can also hyperlink to images that are public


def fill_optional_values(data):
    if not "id" in data:
        data["id"] = generate_random_string()


def add_categories(post, raw_data):
    if "categories" in raw_data:
        # slow, but good enough for now....
        current = Category.objects.all().filter(post=post)
        for category in current:
            category.delete()
        for category in list(raw_data["categories"]):
            Category(category=category, post=post).save()

#  https://www.django-rest-framework.org/tutorial/3-class-based-views/


class PostList(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/"""

    def get(self, request, id, format=None):
        """GET [local, remote] get the recent posts from post AUTHOR_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        posts = Post.objects.all().filter(author=id)

        if request.app_session.author != author:
            posts = posts.filter(unlisted=False)

        posts = posts.order_by("-published")
        posts = paginate(request, posts)

        dict = {"type": "posts", "items": process_posts(posts)}
        return Response(dict, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, id, format=None):
        """POST [local] create a new post but generate a new id"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        d = request.data
        fill_optional_values(d)
        d["author"] = id
        serializer = PostSerializer(data=d)

        if serializer.is_valid():
            post = serializer.save(id=d["id"])
            add_categories(post, d)
            # add the post to the inbox of each of the author's followers
            send_to_all_followers(author, post)
            return Response({"id": post.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostImage(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image"""

    def get(self, request, author_id, post_id):
        """GET [local, remote] get the image contents of a post, or return a 404 if the post is not an image"""
        # ensure author exists and is authorized
        post = get_object_or_404(Post.objects.all().filter(author=author_id), id=post_id)
        if not post.contentType in [ContentType.JPEG, ContentType.PNG]:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(base64.b64decode(post.content),
                            content_type=post.contentType.split(";")[0])


class PostDetail(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    POST [local] update the post whose id is POST_ID (must be authenticated)"""

    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the public post whose id is POST_ID"""
        # ensure author exists and is authorized
        post = get_object_or_404(Post, id=post_id)  # id is unique (don't need author_id)
        data = serialize_single_post(post)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, author_id, post_id, format=None):
        """PUT [local] create a post where its id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)

        post = get_object_or_404(Post, id=post_id, author=author_id)
        request.data["author"] = author_id
        serializer = PostSerializer(post, data=request.data)  # overwrite post with request.data
        if serializer.is_valid():
            post = serializer.save()
            add_categories(post, request.data)
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id, post_id, format=None):
        """DELETE [local] remove the post whose id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_200_OK)

############
# COMMENTS #
############


class CommentList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments"""

    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the list of comments of the post whose id is POST_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get the post
        post = get_object_or_404(Post, id=post_id)
        # get all comments for the post
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        dict = {"type": "comments", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request, author_id, post_id, format=None):
        """
        POST [local] if you post an object of “type”:”comment”,
        it will add your comment to the post whose id is POST_ID
        """
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post exists
        post = get_object_or_404(Post, id=post_id)

        # add ids to request.data for serializer
        request.data["author"] = author_id
        request.data["post"] = post_id
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save()
            # add the comment to the inbox of the post author and all of their followers
            send_to_all_followers(post.author, comment)
            return Response({"id": comment.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#########
# LIKED #
#########

class LikedList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/liked"""

    def get(self, request, author_id, format=None):
        """GET [local, remote] list what public things AUTHOR_ID liked."""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get all of the author's post likes
        post_likes = author.post_likes.all()
        serializer1 = PostLikeSerializer(post_likes, many=True)
        # add all of the author's comment likes
        comment_likes = author.comment_likes.all()
        serializer2 = CommentLikeSerializer(comment_likes, many=True)

        # TODO: Figure out how to properly combine two serializers
        arr = []
        for serializer in [serializer1.data, serializer2.data]:
            for data in serializer:
                arr.append(dict(data))
        return Response({"type": "liked", "items": arr}, status=status.HTTP_200_OK)

##############
# POST LIKES #
##############


class PostLikeList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes"""

    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID"""

        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Post, id=post_id)
        likes = post.likes.all()
        serializer = PostLikeSerializer(likes, many=True)
        dict = {"type": "likes", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request, author_id, post_id, format=None):
        "POST a like for a particular post"
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post and comment exist
        post = get_object_or_404(Post, id=post_id)
        # save a new like for this post
        like = post.likes.create(author=post.author)
        # add the like to the inbox of the post's author and all of their followers
        send_to_all_followers(post.author, like)
        return Response(status=status.HTTP_201_CREATED)


#################
# COMMENT LIKES #
#################

class CommentLikeList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes"""

    def get(self, request, author_id, post_id, comment_id, format=None):
        """POST a 'like' to a particular comment"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # get the comment we're looking for
        comment = get_object_or_404(Comment, id=comment_id)
        comment_likes = comment.likes.all()
        serializer = CommentLikeSerializer(comment_likes, many=True)
        dict = {"type": "likes", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request, author_id, post_id, comment_id, format=None):
        """POST a 'like' to a particular comment"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post and comment exist
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        # save a new like for this comment
        like = comment.likes.create(author=author)
        # add the like to the inbox of the post author and all of their followers
        send_to_all_followers(post.author, like)
        return Response({"id": like.id}, status=status.HTTP_201_CREATED)