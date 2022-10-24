from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Inbox
from authors.models import Author
from .serializers import InboxSerializer

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

def create_new_inbox(author) -> None:
    """Creates a new inbox for an author"""
    inbox = Inbox(author=author)
    inbox.save()


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class InboxList(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/"""
        
    def get(self, request, id, format=None):
        """# GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)"""
        author = get_object_or_404(Author, id=id) #TODO: Authentication handling
        author.check_authorization()
        inbox = get_object_or_404(Inbox, author_id=author)
        posts = inbox.get_data(Inbox.DataType.POST) # get a list of posts sent to AUTHOR_ID (rubric specifies posts?)
        serializer = InboxSerializer(posts,many=True) #TODO: handle getting other data from inbox as well
        dict = {"type": "inbox", "author": author.id, "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    
    def post(self, request, id, format=None):
        """# POST [local, remote]: send a post to the author"""

        request.data["author"] = id
        serializer = InboxSerializer(data=request.data)

        if serializer.is_valid():
            post: Inbox = serializer.save()
            serializer_data = {"id":post.id}
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)