from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.models import Author
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from authors.serializers import AuthorSerializer
from inbox.views import add_data_to_inboxes_of_followers

# Be aware that Posts can be images that need base64 decoding.
# posts can also hyperlink to images that are public


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class PostList(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/"""
        
    def get(self, request, id, format=None):
        """GET [local, remote] get the recent posts from post AUTHOR_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        posts = Post.objects.all().filter(author=id)
        serializer = PostSerializer(posts,many=True)
        dict = {"type": "posts", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    
    def post(self, request, id, format=None):
        """POST [local] create a new post but generate a new id"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        request.data["author"] = id
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            post = serializer.save() 
            # add the post to the inbox of each of the author's followers
            add_data_to_inboxes_of_followers(author, post)
            return Response({"id":post.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    POST [local] update the post whose id is POST_ID (must be authenticated)"""

    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the public post whose id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, id=post_id) # id is unique (don't need author_id)
        post_serializer = PostSerializer(post).data
        author = AuthorSerializer(author).data
        post_serializer["author"] = author
        post_serializer["count"] = len(Comment.objects.filter(post=post))
        return Response(post_serializer, status=status.HTTP_200_OK)
    
    def put(self, request, author_id, post_id, format=None):
        """PUT [local] create a post where its id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        post = get_object_or_404(Post, id=post_id, author=author_id)
        request.data["author"] = author_id
        serializer = PostSerializer(post,data=request.data) # overwrite post with request.data
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, author_id, post_id, format=None):
        """DELETE [local] remove the post whose id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_200_OK)
    
############
# COMMENTS #  
############
    
class CommentList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments"""
        
    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the list of comments of the post whose id is POST_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # get the post
        post = get_object_or_404(Post, id=post_id)
        # get all comments for the post
        comments = post.comments.all()
        serializer = CommentSerializer(comments,many=True)
        dict = {"type": "comments", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    
    def post(self, request, author_id, post_id, format=None):
        """
        POST [local] if you post an object of “type”:”comment”,
        it will add your comment to the post whose id is POST_ID
        """
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post exists
        get_object_or_404(Post, id=post_id)

        # add ids to request.data for serializer
        request.data["author"] = author_id
        request.data["post"] = post_id
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save()
            # add the comment to the inbox of each of the author's followers
            add_data_to_inboxes_of_followers(author, comment)
            return Response({"id":comment.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#########
# LIKED #  
######### 

class LikedList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/liked"""
    def get(self, request, author_id, format=None):
        """GET [local, remote] list what public things AUTHOR_ID liked."""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # get all of the author's post likes
        post_likes = author.post_likes.all()
        serializer1 = PostLikeSerializer(post_likes,many=True)
        # add all of the author's comment likes
        comment_likes = author.comment_likes.all()
        serializer2 = CommentLikeSerializer(comment_likes,many=True)

        #TODO: Figure out how to properly combine two serializers
        arr = []
        for serializer in [serializer1.data,serializer2.data]:
            for data in serializer:
                arr.append(dict(data))
        return Response({"type": "liked", "items": arr}, status=status.HTTP_200_OK)
    
##############
# POST LIKES #  
##############

class PostLikeList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes"""
        
    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID"""

        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        post = get_object_or_404(Post,id=post_id)
        likes = post.likes.all()
        serializer = PostLikeSerializer(likes,many=True)
        dict = {"type": "likes", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
    

    def post(self, request, author_id, post_id, format=None):
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post and comment exist
        post = get_object_or_404(Post, id=post_id)
        # save a new like for this post
        post.likes.create(author=post.author)
        return Response(status=status.HTTP_201_CREATED)

    
#################
# COMMENT LIKES #  
#################
    
class CommentLikeList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes"""
        
    def get(self, request, author_id, post_id, comment_id, format=None):
        """POST a 'like' to a particular comment"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # get the comment we're looking for
        comment = get_object_or_404(Comment, id=comment_id)
        comment_likes = comment.likes.all()
        serializer = CommentLikeSerializer(comment_likes,many=True)
        dict = {"type": "likes", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
 
    def post(self, request, author_id, post_id, comment_id, format=None):
        """POST a 'like' to a particular comment"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post and comment exist
        get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        # save a new like for this comment
        like = comment.likes.create(author=author)
        # add the like to the inboxes of all followers of this author
        add_data_to_inboxes_of_followers(author,like)
        return Response({"id": like.id}, status=status.HTTP_201_CREATED)
