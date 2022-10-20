from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Follower
from .serializers import AuthorSerializer

#  https://www.django-rest-framework.org/tutorial/3-class-based-views/

# /authors/ GET, POST
class AuthorList(APIView):
        
    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer_arr = []
        for author in authors:
            serializer = AuthorSerializer(author)
            serializer_data = serializer.data
            serializer_data["id"] = author.get_full_path()
            serializer_data["url"] = author.get_full_path()
            serializer_arr.append(serializer_data)
        dict = {"type": "authors", "items": serializer_arr}
        return Response(dict, status=status.HTTP_200_OK)

    
    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
         # if valid user input
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        # else failed POST attempt
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /authors/<id> GET, POST
class AuthorDetail(APIView):

    def get(self, request, id, format=None):
        
        author = get_object_or_404(Author, id=id)
        serializer = AuthorSerializer(author)
        serializer_data = serializer.data
        serializer_data["id"] = author.get_full_path()
        serializer_data["url"] = author.get_full_path()
        return Response(serializer_data, status=status.HTTP_200_OK)
    

class FollowerList(APIView):
        
    def get(self, request, id, format=None):
        """Get all followers of a specified Author"""
        author = get_object_or_404(Author, id=id)
        followers = author.followers.all()
        serializer = AuthorSerializer(followers, many=True)
        dict = {"type": "followers", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    
    # def post(self, request, format=None):

    #     serializer = FollowerSerializer(data=request.data)
    #      # if valid user input
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_200_OK)
    #     # else failed POST attempt
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /authors/<id> GET, POST
class FollowerDetail(APIView):

    def get(self, request, author_id, follower_id, format=None):
        """Get a specific Author that is following another specific Author"""

        author = get_object_or_404(Author, id=author_id)
        followers = author.followers.all()
        follower = get_object_or_404(followers, id=follower_id)
        serializer = AuthorSerializer(follower)
        serializer_data = serializer.data
        serializer_data["id"] = author.get_full_path()
        serializer_data["url"] = author.get_full_path()
        return Response(serializer_data, status=status.HTTP_200_OK)
    
    def put(self, request, author_id, follower_id, format=None):
        """Add an Author as a follower of another Author"""
        author = get_object_or_404(Author, id=author_id)
        follower = get_object_or_404(Author, id=follower_id)
        author.followers.add(follower)
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, author_id, follower_id, format=None):
        """Remove an Author as a follower of another Author"""
        author = get_object_or_404(Author, id=author_id)
        followers = author.followers.all()
        follower = get_object_or_404(followers, id=follower_id)
        author.followers.remove(follower)
        return Response(status=status.HTTP_200_OK)