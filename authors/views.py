from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django import http

from .models import Author
from .serializers import AuthorSerializer
from nodes.models import Node
from nodes.serializers import NodeSerializer

#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class AuthorList(APIView):
    """/authors/ GET, POST"""
        
    def get(self, request, format=None):
        """GET [local, remote]: retrieve all profiles on the server (paginated)
        page: how many pages
        size: how big is a page
        Example query: GET ://service/authors?page=10&size=5
        Gets the 5 authors, authors 45 to 49.
        """
        def get_authors_from_nodes():
            nodes = Node.objects.all() # TODO: filter out node for this server
            arr = []
            for node in nodes:
                authors_url = node.host + "/authors/"
                response = requests.get(authors_url, auth=(node.username, node.password))
                arr.append(response.json())
            return http.JsonResponse(arr)

            
        authors = Author.objects.filter(isAuthorized=True) # only get authorized authors
        serializer_arr = []
        for author in authors:
            serializer = AuthorSerializer(author)
            serializer_data = serializer.data
            serializer_arr.append(serializer_data)
        
        # response = get_authors_from_nodes()
        # print(response)
        # TODO: add response data to serializer_arr

        dict = {"type": "authors", "items": serializer_arr}
        return Response(dict, status=status.HTTP_200_OK)

    
    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
         # if valid user input
        if serializer.is_valid():
            author = serializer.save()
            return Response({"id":author.id}, status=status.HTTP_201_CREATED)
        # else failed POST attempt
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):
    """/authors/<id> GET, POST"""

    def get(self, request, id, format=None):
        """GET [local, remote]: retrieve AUTHOR_ID’s profile"""
        
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = AuthorSerializer(author)
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)
    
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


class FollowingList(APIView):
    """/authors/<id>/following/ GET"""
        
    def get(self, request, id, format=None):
        """Get all Author's that an Author is following"""
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # exclude the current author from authors
        authors = Author.objects.filter(isAuthorized=True).exclude(id=id)

        for a in authors:
            followers_of_a = a.followers.all()
            # exclude a from queryset if author is not following a
            if author not in followers_of_a:
                authors = authors.exclude(id=a.id)
                
        # authors is now a queryset of Author objects that author is following
        serializer = AuthorSerializer(authors, many=True)
        dict = {"type": "following", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
    

class FollowerList(APIView):
    """/authors/<id>/followers/ GET"""
        
    def get(self, request, id, format=None):
        """Get all followers of a specified Author"""
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        followers = author.followers.all()
        serializer = AuthorSerializer(followers, many=True)
        dict = {"type": "followers", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class FollowerDetail(APIView):
    """/authors/<author_id>/followers/<follower_id> GET, PUT, DELETE"""

    def get(self, request, author_id, follower_id, format=None):
        """Get a specific Author that is following another specific Author"""
        # ensure author exists
        author = get_object_or_404(Author, id=author_id)
        followers = author.followers.all()
        # ensure follower is actually a follower of author
        follower: Author = get_object_or_404(followers, id=follower_id)
        # ensure both are authorized
        for a in [author,follower]:
            if not a.isAuthorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = AuthorSerializer(follower)
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)
    
    def put(self, request, author_id, follower_id, format=None):
        """Add an Author as a follower of another Author"""
        # ensure author and follower exist and are both authorized
        author = get_object_or_404(Author, id=author_id)
        follower_id = follower_id.split("/authors/")[1]
        follower = get_object_or_404(Author, id=follower_id)
        for a in [author,follower]:
            if not a.isAuthorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        # prevent author from adding self as follower
        if author_id == follower_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        author.followers.add(follower)  # this adds the entry to the Follower table
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, author_id, follower_id, format=None):
        """Remove an Author as a follower of another Author"""
        author = get_object_or_404(Author, id=author_id)
        followers = author.followers.all()
        follower_id = follower_id.split("/authors/")[1]
        follower = get_object_or_404(followers, id=follower_id)
        author.followers.remove(follower)
        return Response(status=status.HTTP_200_OK)