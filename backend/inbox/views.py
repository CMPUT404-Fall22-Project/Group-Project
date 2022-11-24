from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from posts.serializers import CommentSerializer, CommentLikeSerializer, PostLikeSerializer
from django.http import JsonResponse
from utils.proxy import fetch_author, get_authorization_from_url, Ref
from utils.requests import paginate
from authors.models import Author, Follower, get_scheme_and_netloc
from .models import Inbox
from .serializers import InboxSerializer
from authors.serializers import AuthorSerializer
from utils.process_models import serialize_single_post, serialize_single_comment
import requests
from requests import HTTPError
from utils.requests import get_optionally_list_parameter_or_default
from django.core.exceptions import PermissionDenied

# Inbox
# The inbox is all the new posts from who you follow
# URL: ://service/authors/{AUTHOR_ID}/inbox
# GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
# POST [local, remote]: send a post to the author
# if the type is “post” then add that post to AUTHOR_ID’s inbox
# if the type is “follow” then that follow is added to AUTHOR_ID’s inbox to approve later
# if the type is “like” then add that like to AUTHOR_ID’s inbox
# if the type is “comment” then add that comment to AUTHOR_ID’s inbox


def send_to_all_followers(author: Author, data):
    """
    Saves data to the inboxes of all followers of an author
    @params: author - The Author whose followers will receive the data to their inboxes
            data - A Post, Follow, Like, or Comment
    """
    # get the correct serializer
    if data.type == "post":
        serialized = serialize_single_post(data)
        serialized["type"] = data.type
    elif data.type == "comment":
        serialized = serialize_single_comment(data)
        serialized["type"] = data.type
    else:
        if hasattr(data, "comment"):
            serialized = CommentLikeSerializer(data).data
            serialized["type"] = "comment"
        else:
            serialized = PostLikeSerializer(data).data
            serialized["type"] = "like"
    # add to inbox of all of the author's followers
    followerUrls = Follower.objects.all().filter(
        author=author).values_list("follower", flat=True)

    for followerUrl in followerUrls:
        url = followerUrl + "/inbox/"  # id is the full URL because it's remote
        result = requests.post(url, serialized, headers={'Authorization': get_authorization_from_url(url)})
        if result.status_code >= 300:
            raise HTTPError(f"POST to server at {url} failed! msg={result.text}")


# sorry aaron, this is all i know.


@api_view(["GET"])
def filter_inbox(request, author_id):
    """
    URL: ://service/authors/{AUTHOR_ID}/inbox/filter/

    Searches the inbox and returns the 
    params:
        types[]: Array of types to filter by
        [page | 0]: The result page
        [size | 5]: The number of results to return
    """
    types = get_optionally_list_parameter_or_default(request, "types", [])
    author = get_object_or_404(Author, id=author_id)
    if request.app_session.author != author:
        raise PermissionDenied("Unauthorizeed access to inbox")
    # get all of the inbox items for this author
    inbox = paginate(request, Inbox.objects.filter(author=author, dataType__in=types))
    serializer = InboxSerializer(inbox, many=True)
    items = [Ref(x["data"]).as_data() for x in serializer.data]
    dictionary = {"type": "inbox", "author": author.id, "items": items}
    return JsonResponse(dictionary, safe=False)


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class InboxList(APIView):
    """ URL: ://service/authors/{AUTHOR_ID}/inbox """

    def get(self, request, id, format=None):
        """GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)"""
        author = get_object_or_404(Author, id=id)
        if request.app_session.author != author:
            raise PermissionDenied("Unauthorizeed access to inbox")
        # get all of the inbox items for this author
        inbox = paginate(request, Inbox.objects.filter(author=author))
        serializer = InboxSerializer(inbox, many=True)
        items = [Ref(x["data"]).as_data() for x in serializer.data]
        dictionary = {"type": "inbox", "author": author.id, "items": items}

        return Response(dictionary, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        """
        POST [local, remote]: send a post to the author
        if the type is “post” then add that post to AUTHOR_ID's inbox
        if the type is “follow” then add that follow is added to AUTHOR_ID's inbox to approve later
        if the type is “like” then add that like to AUTHOR_ID's inbox
        if the type is “comment” then add that comment to AUTHOR_ID's inbox
        """
        # ensure the author exists and is authorized
        author = get_object_or_404(Author, id=id)

        # get the data type
        type = request.data["type"]

        if type == "post":
            data = request.data
            ref = Ref(data)
            inbox = author.inboxes.create(data=ref.as_ref(), dataType=type)
            return Response({"id": inbox.id}, status=status.HTTP_201_CREATED)
        if type in ["like", "comment"]:
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
            data["summary"] = str(follower.displayName) + " wants to follow " + author.displayName
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
