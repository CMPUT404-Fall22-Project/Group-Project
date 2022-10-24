from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


# Be aware that Posts can be images that need base64 decoding.
# posts can also hyperlink to images that are public


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class PostList(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/"""
        
    def get(self, request, id, format=None):
        """GET [local, remote] get the recent posts from post AUTHOR_ID (paginated)"""
        # author = get_object_or_404(Author, id=id) TODO: ensure author exists?
        posts = Post.objects.all().filter(author=id)
        serializer = PostSerializer(posts,many=True)
        dict = {"type": "posts", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    
    def post(self, request, id, format=None):
        """POST [local] create a new post but generate a new id"""

        request.data["author"] = id
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            post: Post = serializer.save()
            serializer_data = {"id":post.id}
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    POST [local] update the post whose id is POST_ID (must be authenticated)"""

    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the public post whose id is POST_ID"""
        post = get_object_or_404(Post, id=post_id) # id is unique (don't need author_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, author_id, post_id, format=None):
        """PUT [local] create a post where its id is POST_ID"""
        post = get_object_or_404(Post, id=post_id, author=author_id)
        request.data["author"] = author_id
        serializer = PostSerializer(post,data=request.data) # overwrite post with request.data
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, author_id, post_id, format=None):
        """DELETE [local] remove the post whose id is POST_ID"""
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_200_OK)