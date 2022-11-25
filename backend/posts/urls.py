from django.urls import path

from .views import PostDetail, PostImage, PostList, AllPostList, \
CommentList, LikedList, PostLikeList, CommentLikeList, add_new_comment

urlpatterns = [
    # posts
    path("posts/", AllPostList.as_view(), name="all_post_list"),
    path("authors/<id>/posts/", PostList.as_view(), name="post_list"),
    path("authors/<author_id>/posts/<post_id>/image", PostImage.as_view(), name="post_list"),
    path("authors/<author_id>/posts/<post_id>", PostDetail.as_view(), name="post_detail"),
    # comments
    path("authors/<author_id>/posts/<post_id>/comments", CommentList.as_view(), name="comment_list"),
    path("authors/<author_id>/posts/<post_id>/comments/new/", add_new_comment, name="comment_list"),
    # likes
    path("authors/<author_id>/liked/", LikedList.as_view(), name="liked_list"),
    path("authors/<author_id>/posts/<post_id>/likes", PostLikeList.as_view(), name="post_like_list"),
    path("authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes",
         CommentLikeList.as_view(), name="comment_like_list"),
]
