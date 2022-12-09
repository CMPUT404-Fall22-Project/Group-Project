from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from utils.model_utils import get_host
from utils.constants import MY_CLIENT
from utils.proxy import fetch_author
from .models import Author, Follower
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.swagger_data import SwaggerData
from .serializers import AuthorSerializer
from authentication.models import ExternalNode
from utils.auth import authenticated


class AllAuthorList(APIView):
    """/authors/all/ GET"""
    
    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    SwaggerData.author_list
                }
            )
        }
    )
    def get(self, request, format=None):
        """GET [local, remote]: retrieve all profiles across all servers, including own (paginated)
        page: how many pages
        size: how big is a page
        Example query: GET ://service/authors/all/?page=10&size=5
        Gets the 5 authors, authors 45 to 49.
        """
        def get_authors_from_remote_nodes():
            """GET all authors across all remote nodes"""
            nodes = ExternalNode.objects.exclude(host=get_host())
            authors = []
            for node in nodes:
                authors_url =  node.api + "authors"
                response = requests.get(authors_url, headers={'Authorization': node.authorization})
                if response.status_code >= 300:
                    print(f'authors/all -> {authors_url}: HTTP{response.status_code} - {response.text}\n') # print the error
                    continue
                
                data = response.json()
                if isinstance(data, list):
                    authors.extend(data)
                else:
                    for author in data["items"]:
                        authors.append(author)
            return authors

        # Get local authors
        local_authors = Author.objects.filter(isAuthorized=True)
        serializer = AuthorSerializer(local_authors,many=True)
        serializer_data: list = serializer.data
        
        # get remote authors
        remote_authors = get_authors_from_remote_nodes()
        for author in remote_authors:
            serializer_data.append(author)

        dict = {"type": "authors", "items": serializer_data}
        return Response(dict, status=status.HTTP_200_OK)


class AuthorList(APIView):
    """/authors/ GET, POST"""
    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    SwaggerData.author_list
                }
            )
        }
    )
    def get(self, request, format=None):
        """GET [local, remote]: retrieve all profiles on the server (paginated)
        page: how many pages
        size: how big is a page
        Example query: GET ://service/authors?page=10&size=5
        Gets the 5 authors, authors 45 to 49.
        """
        authors = Author.objects.filter(isAuthorized=True)
        serializer = AuthorSerializer(authors,many=True)
        dict = {"type": "authors", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING),
                "id": openapi.Schema(type=openapi.TYPE_STRING),
                "host": openapi.Schema(type=openapi.TYPE_STRING),
                "displayName": openapi.Schema(type=openapi.TYPE_STRING),
                "url": openapi.Schema(type=openapi.TYPE_STRING),
                "github": openapi.Schema(type=openapi.TYPE_STRING),
                "profileImage": openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    @authenticated
    def post(self, request, format=None):
        """POST [local]: add an author to /authors"""
        serializer = AuthorSerializer(data=request.data)
        # if valid user input
        if serializer.is_valid():
            author = serializer.save()
            return Response({"id": author.id}, status=status.HTTP_201_CREATED)
        # else failed POST attempt
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):
    """/authors/<id> GET, POST"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    SwaggerData.author_detail
                }
            )
        }
    )
    def get(self, request, id, format=None):
        """GET [local, remote]: retrieve AUTHOR_ID’s profile"""

        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = AuthorSerializer(author)
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING),
                "id": openapi.Schema(type=openapi.TYPE_STRING),
                "host": openapi.Schema(type=openapi.TYPE_STRING),
                "displayName": openapi.Schema(type=openapi.TYPE_STRING),
                "url": openapi.Schema(type=openapi.TYPE_STRING),
                "github": openapi.Schema(type=openapi.TYPE_STRING),
                "profileImage": openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    @authenticated
    def post(self, request, id, format=None):
        """POST [local]: update AUTHOR_ID’s profile"""
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # serialize the author and set the attributes to the request.data values
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response(status=status.HTTP_200_OK)
        # else failed POST attempt
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowerList(APIView):
    """/authors/<id>/followers/ GET"""
    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    SwaggerData.follower_list
                }
            )
        }
    )
    def get(self, request, id, format=None):
        """Get all followers of a specified Author"""
        author = get_object_or_404(Author, id=id)
        followers = Follower.objects.all().filter(author=author).values_list("follower", flat=True)

        serializer = AuthorSerializer([fetch_author(x) for x in followers], many=True)
        dict = {"type": "followers", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


def find_follower(author_id, follower_id):
    author = get_object_or_404(Author, id=author_id)
    followers = Follower.objects.all().filter(author=author).values_list("follower", flat=True)
    for x in followers:
        f = fetch_author(x)
        print(x)
        if x == follower_id or f.id == follower_id:
            return (author, x, f)
    return (author, None, None)


class FollowerDetail(APIView):
    """/authors/<author_id>/followers/<follower_id> GET, PUT, DELETE"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    SwaggerData.author_detail
                }
            )
        }
    )
    def get(self, request, author_id, follower_id, format=None):
        """Get a specific Author that is following another specific Author"""
        # ensure author exists
        _, followObj, follower = find_follower(author_id, follower_id)
        if (follower != None):
            return Response({"isFollowing": True, "isAccepted": followObj.isAccepted}, status=status.HTTP_200_OK)
        return Response({"isFollowing": False, "isAccepted": False}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING),
                "id": openapi.Schema(type=openapi.TYPE_STRING),
                "host": openapi.Schema(type=openapi.TYPE_STRING),
                "displayName": openapi.Schema(type=openapi.TYPE_STRING),
                "url": openapi.Schema(type=openapi.TYPE_STRING),
                "github": openapi.Schema(type=openapi.TYPE_STRING),
                "profileImage": openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )

    @authenticated
    def put(self, request, author_id, follower_id, format=None):
        """Add an Author as a follower of another Author"""
        Follower(author=get_object_or_404(Author, pk=author_id),
                 follower=follower_id).save()  # this adds the entry to the Follower table
        return Response(status=status.HTTP_200_OK)

    @authenticated
    def delete(self, request, author_id, follower_id, format=None):
        """Remove an Author as a follower of another Author"""
        follower = get_object_or_404(Follower, author=get_object_or_404(Author, pk=author_id), follower=follower_id)
        follower.delete()
        return Response(status=status.HTTP_200_OK)
