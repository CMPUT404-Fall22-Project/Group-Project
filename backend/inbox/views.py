from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from posts.serializers import CommentSerializer, CommentLikeSerializer, PostLikeSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from authors.models import Author
from .models import Inbox
from .serializers import InboxSerializer
from authors.serializers import AuthorSerializer


# Inbox
# The inbox is all the new posts from who you follow
# URL: ://service/authors/{AUTHOR_ID}/inbox
# GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
# POST [local, remote]: send a post to the author
# if the type is “post” then add that post to AUTHOR_ID’s inbox
# if the type is “follow” then that follow is added to AUTHOR_ID’s inbox to approve later
# if the type is “like” then add that like to AUTHOR_ID’s inbox
# if the type is “comment” then add that comment to AUTHOR_ID’s inbox

def add_data_to_inboxes_of_author_and_followers(author: Author, data):
    """
    Saves data to the inboxes of all followers of an author
    @params: author - The Author whose followers will receive the data to their inboxes
            data - A Post, Follow, Like, or Comment
    """
    # get the correct serializer
    if data.type == "post":
        serializer = PostSerializer(data)
    elif data.type == "comment":
        serializer = CommentSerializer(data)
    else:
        if hasattr(data, "comment"):
            serializer = CommentLikeSerializer(data)
        else:
            serializer = PostLikeSerializer(data)
    # add to the author's inbox
    author.inboxes.create(data=serializer.data, dataType=data.type)
    # add to inbox of all of the author's followers
    for author in author.followers.all():
        author.inboxes.create(data=serializer.data, dataType=data.type)


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class InboxList(APIView):
    """ URL: ://service/authors/{AUTHOR_ID}/inbox """

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    {
                        "type": "inbox",
                        "author": "http://127.0.0.1:5454/authors/c1e3db8ccea4541a0f3d7e5c75feb3fb",
                        "items": [
                            {
                                "type": "post",
                                "title": "A Friendly post title about a post about web dev",
                                "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                                "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                                "origin": "http://whereitcamefrom.com/posts/zzzzz",
                                "description": "This post discusses stuff -- brief",
                                "contentType": "text/plain",
                                "content": "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge",
                                "author": {
                                    "type": "author",
                                    "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                    "host": "http://127.0.0.1:5454/",
                                    "displayName": "Lara Croft",
                                    "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                    "github": "http://github.com/laracroft",
                                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                },
                                "categories": ["web", "tutorial"],
                                "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                                "published":"2015-03-09T13:07:04+00:00",
                                "visibility":"FRIENDS",
                                "unlisted":False
                            },
                        ]
                    }
                }
            )
        }
    )
    def get(self, request, id, format=None):
        """GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # get all of the inbox items for this author
        inbox = Inbox.objects.filter(author=author)
        serializer = InboxSerializer(inbox, many=True)
        dictionary = {"type": "inbox",
                      "author": author.id, "items": serializer.data}

        return Response(dictionary, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING),
                "summary": openapi.Schema(type=openapi.TYPE_STRING),
                "actor": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                "object": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    def post(self, request, id, format=None):
        """
        POST [local, remote]: send a post to the author.
        *if the type is “post” then add that post to AUTHOR_ID’s inbox*
        *if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later*
        *if the type is “like” then add that like to AUTHOR_ID’s inbox*
        *if the type is “comment” then add that comment to AUTHOR_ID’s inbox*
        This request_body example contains a follow request example.
        Please see the Like, Comment, and Post objects for the other possible inbox request_body examples.
        """
        # ensure the author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get the data type
        type = request.data["type"]

        if type in ["post", "like", "comment"]:
            # save the data to the author's inbox
            data = request.data
            del data["type"]  # this key/value be saved under dataType
            inbox = author.inboxes.create(data=request.data, dataType=type)
            return Response({"id": inbox.id}, status=status.HTTP_201_CREATED)

        if type == "follow":
            # ensure the follower exists and is authorized
            follower_id = request.data["id"]
            follower_id = follower_id.split("/authors/")[1]
            follower = get_object_or_404(Author, id=follower_id)
            if not follower.isAuthorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            # Create the follow request (we only need the ids of the authors)
            author_serializer = AuthorSerializer(author)
            follower_serializer = AuthorSerializer(follower)
            data = {}
            data["type"] = "follow"
            data["summary"] = str(follower.displayName) + \
                " wants to follow " + author.displayName
            data["actor"] = follower_serializer.data
            data["object"] = author_serializer.data

            inbox = author.inboxes.create(data=data, dataType=data["type"])
            return Response({"id": inbox.id}, status=status.HTTP_201_CREATED)

    def delete(self, request, id, format=None):
        """DELETE [local]: clear the inbox"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # delete all of the inbox items for this author
        inbox = Inbox.objects.filter(author=author)
        for item in inbox:
            item.delete()
        return Response(status=status.HTTP_200_OK)


class InboxDetail(APIView):

    def delete(self, request, author_id, inbox_id, format=None):
        """Delete from inbox by id"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # get and delete the inbox item
        inbox = get_object_or_404(Inbox, id=inbox_id)
        inbox.delete()
        return Response(status=status.HTTP_200_OK)
