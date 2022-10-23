from django.urls import path

from .views import PostDetail, PostList

urlpatterns = [
    path("authors/<id>/posts/", PostList.as_view(), name="post_list"),
    path("authors/<author_id>/posts/<post_id>", PostDetail.as_view(), name="post_detail")
]