from django.urls import path

from .views import AllAuthorList, AuthorDetail, AuthorList, FollowerDetail, FollowerList

urlpatterns = [
    path("authors/all/", AllAuthorList.as_view(), name="all_author_list"),
    path("authors/", AuthorList.as_view(), name="author_list"),
    path("authors/<id>", AuthorDetail.as_view(), name="author_detail"),
    path("authors/<id>/followers/", FollowerList.as_view(), name="follower_list"),
    path("authors/<id>/followers", FollowerList.as_view(), name="follower_list"),
    path("authors/<author_id>/followers/<path:follower_id>", FollowerDetail.as_view(),
         name="follower_detail"),  # path: allows for forward slashes in arg

]
# NOTE: Do we need FollowingList?