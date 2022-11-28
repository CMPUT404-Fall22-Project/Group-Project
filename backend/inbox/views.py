from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.swagger_data import SwaggerData
from posts.serializers import CommentSerializer, CommentLikeSerializer, PostLikeSerializer
from django.http import JsonResponse
from utils.proxy import fetch_author, get_authorization_from_url, get_host_from_url, Ref
from utils.requests import paginate
from authors.models import Author, Follower
from .models import Inbox
from .serializers import InboxSerializer
from authors.serializers import AuthorSerializer
from utils.process_models import serialize_single_post, serialize_single_comment
import requests
from requests import HTTPError
from utils.requests import get_optionally_list_parameter_or_default
from django.core.exceptions import PermissionDenied
from django.http import Http404
from authentication.models import ExternalNode
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from utils.auth import authenticated

# Inbox
# The inbox is all the new posts from who you follow
# URL: ://service/authors/{AUTHOR_ID}/inbox
# GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
# POST [local, remote]: send a post to the author
# if the type is “post” then add that post to AUTHOR_ID’s inbox
# if the type is “follow” then that follow is added to AUTHOR_ID’s inbox to approve later
# if the type is “like” then add that like to AUTHOR_ID’s inbox
# if the type is “comment” then add that comment to AUTHOR_ID’s inbox


def serialize_data(data):
    serialized = None
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
    return serialized


def send_to_all_followers(author: Author, data):
    """
    Saves data to the inboxes of all followers of an author
    @params: author - The Author whose followers will receive the data to their inboxes
            data - A Post, Follow, Like, or Comment
    """
    # get the correct serializer
    serialized = serialize_data(data)
    # add to inbox of all of the author's followers
    followerUrls = Follower.objects.all().filter(
        author=author).values_list("follower", flat=True)

    for followerUrl in followerUrls:
        url = followerUrl + "/inbox/"  # id is the full URL because it's remote
        result = requests.post(url, serialized, headers={'Authorization': get_authorization_from_url(url)})
        if result.status_code >= 300:
            raise HTTPError(f"POST to server at {url} failed! msg={result.text}")


def send_to_user(authorUrl, data):
    serialized = serialize_data(data)
    result = requests.post(authorUrl, serialized, headers={'Authorization': get_authorization_from_url(authorUrl)})
    if result.status_code >= 300:
        raise HTTPError(f"POST to server at {authorUrl} failed! msg={result.text}")

    return serialized


# sorry aaron, this is all i know.
def dereference_inbox(qs):
    items = []
    for x in qs:
        if x.dataType != "post":
            items.append(InboxSerializer(x).data["data"])
        else:
            try:
                items.append(Ref(InboxSerializer(x).data["data"]).as_data())
            except Http404:
                x.delete()  # remove from the inbox...
    return items


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
    inbox = paginate(request, Inbox.objects.filter(author=author, dataType__in=types).order_by("-id"))
    dictionary = {"type": "inbox", "author": author.id, "items": dereference_inbox(inbox)}
    return JsonResponse(dictionary, safe=False)


@api_view(["POST"])
@authenticated
def handle_follow_request(request):
    """
    URL: ://service/handle_follow_request/

    Creates a Follow Request object from the authorId of sender and JSON Author receiver
    Sends a POST request to the receiver's inbox with the Follow Request object as the body

    @params: request.data["senderAuthorURL"] = The URL of the Author that is sending the follow request
             request.data["receiverAuthor"] = The JSON Author that is receiving the follow request
    NOTE: actor is the author that is sending the Follow Request
          object is the author that is receiving the Follow Request
    """

    # sender is a local author
    sender_id = request.data["senderAuthorURL"].split("/authors/")[1]
    actor = get_object_or_404(Author, id=sender_id, isAuthorized=True) # actor is the sender
    object = request.data["receiverAuthor"] # object is the receiver (we already have the data)

    # Generate a follow request
    data = {}
    data["type"] = "follow"
    data["summary"] = str(actor.displayName) + " wants to follow " + object["displayName"]
    data["actor"] = AuthorSerializer(actor).data
    data["object"] = object

    # send a POST request to Inbox of the receiver Author
    url = object["id"] + "/inbox/"
    auth = get_authorization_from_url(object["id"])
    response = requests.post(url, json=data, headers={'Authorization': auth})
    if response.status_code > 202:
        return Response(response.text, status=response.status_code)
    return Response(status=response.status_code)

def mandatory_field(data, field, errs):
    if not field in data:
        errs[field] = "This field is required."

def validate_incoming_inbox_data(data):
    errs = {}
    mandatory_field(data, "type", errs)
    mandatory_field(data, "id", errs)
    if len(errs) > 0:
        raise ValidationError(errs, code=400)

class InboxList(APIView):
    """ URL: ://service/authors/{AUTHOR_ID}/inbox """
    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    SwaggerData.inbox_list
                }
            )
        }
    )
    def get(self, request, id, format=None):
        """GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)"""
        author = get_object_or_404(Author, id=id)
        if request.app_session.author != author:
            raise PermissionDenied("Unauthorizeed access to inbox")
        # get all of the inbox items for this author
        inbox = paginate(request, Inbox.objects.filter(author=author))
        dictionary = {"type": "inbox", "author": author.id, "items": dereference_inbox(inbox)}

        return Response(dictionary, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=SwaggerData.follow_request_body
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    @authenticated
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
        # get the data type
        type = request.data["type"]

        if type == "post":
            validate_incoming_inbox_data(request.data)
            data = request.data
            ref = Ref(data)
            inbox = author.inboxes.create(data=ref.as_ref(), dataType=type)
            return Response({"id": inbox.id}, status=status.HTTP_201_CREATED)

        # else type is "like", "comment", or "follow"
        inbox = author.inboxes.create(data=request.data, dataType=type)
        return Response({"id": inbox.id}, status=status.HTTP_201_CREATED)

    @authenticated
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
    @authenticated
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
