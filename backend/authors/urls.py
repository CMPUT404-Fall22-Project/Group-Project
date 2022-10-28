from django.urls import path

from .views import AuthorDetail, AuthorList, FollowerDetail, FollowerList, FollowingList

urlpatterns = [
    path("authors/", AuthorList.as_view(), name="author_list"),
    path("authors/<id>", AuthorDetail.as_view(), name="author_detail"),
    path("authors/<id>/followers/", FollowerList.as_view(), name="follower_list"),
    path("authors/<author_id>/followers/<follower_id>", FollowerDetail.as_view(), name="follower_detail"),
    path("authors/<id>/following/", FollowingList.as_view(), name="following_list")

]