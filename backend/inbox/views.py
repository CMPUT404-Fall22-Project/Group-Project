from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from posts.serializers import PostSerializer
from authors.models import Author


# Inbox
# The inbox is all the new posts from who you follow
# URL: ://service/authors/{AUTHOR_ID}/inbox
# GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
# POST [local, remote]: send a post to the author
# if the type is “post” then add that post to AUTHOR_ID’s inbox
# if the type is “follow” then that follow is added to AUTHOR_ID’s inbox to approve later
# if the type is “like” then add that like to AUTHOR_ID’s inbox
# if the type is “comment” then add that comment to AUTHOR_ID’s inbox
# DELETE [local]: clear the inbox


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class InboxList(APIView):
    """ URL: ://service/authors/{AUTHOR_ID}/inbox """
        
    def get(self, request, id, format=None):
        """GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # get all of the posts for this author
        posts = Post.objects.all().filter(author=author)
        serializer = PostSerializer(posts,many=True)
        dictionary = {"type":"inbox", "author":id,"items":serializer.data}

        return Response(dictionary, status=status.HTTP_200_OK)

        # q = self.request.GET.get('q', '')
        # if q:
        #     data_type = Inbox.DataType.get_enum(q)
        #     queryset = queryset.filter(state__key=data_type)

        # serializer = InboxSerializer(data,many=True)
        # dict = {"type": "inbox", "author": author.id, "items": serializer.data}
        # return Response(dict, status=status.HTTP_200_OK)

    
    # def post(self, request, id, format=None):
    #     """# POST [local, remote]: send a post to the author"""
    #     print(request.data,"I am the data to be saved to the inbox")

    #     # ensure author exists and is authorized
    #     author = get_object_or_404(Author, id=id)
    #     if not author.isAuthorized:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)

    #     serializer = InboxSerializer(data=request.data)

    #     if serializer.is_valid():
    #         post: Inbox = serializer.save()
    #         id = {"id":post.id}
    #         return Response(id, status=status.HTTP_201_CREATED)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)