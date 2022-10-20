from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from .models import Author
from .serializers import AuthorSerializer, FollowerSerializer

#  https://www.django-rest-framework.org/tutorial/3-class-based-views/

# /authors/ GET, POST
class AuthorList(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404
        
    def get(self, request, fomat=None):
        authors = Author.objects.all()
        serializer_arr = []
        for author in authors:
            serializer = AuthorSerializer(author)
            serializer_data = serializer.data
            serializer_data["id"] = author.get_full_path()
            serializer_data["url"] = author.get_full_path()
            serializer_arr.append(serializer_data)
        return Response(serializer_arr, status=status.HTTP_200_OK)

    
    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
         # if valid user input
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        # else failed POST attempt
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /authors/<pk> GET, POST
class AuthorDetail(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        serializer_data = serializer.data
        serializer_data["id"] = author.get_full_path()
        serializer_data["url"] = author.get_full_path()
        return Response(serializer_data, status=status.HTTP_200_OK)