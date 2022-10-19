from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from .models import Author
from .serializers import AuthorSerializer

#  https://www.django-rest-framework.org/tutorial/3-class-based-views/

# /authors/ GET, POST
class AuthorList(APIView):

    def get(self, request, fomat=None):
        pass

    def post(self, request, format=None):
        pass


# /authors/<pk> GET, POST
class AuthorDetail(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        author = self.get_object(pk)
        pass

    def put(self, request, pk, format=None):
        author = self.get_object(pk)
        pass

    def patch(self, request, pk, format=None):
        author = self.get_object(pk)
        pass

    def delete(self, request, pk, format=None):
        author = self.get_object(pk)
        pass