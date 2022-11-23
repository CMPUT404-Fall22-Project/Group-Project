from django.urls import path

from .views import AuthorDetail, AuthorList, FollowerDetail, FollowerList

urlpatterns = [
    path("authors/", AuthorList.as_view(), name="author_list"),
    path("authors/<id>", AuthorDetail.as_view(), name="author_detail"),
    path("authors/<id>/followers/", FollowerList.as_view(), name="follower_list"),
    path("authors/<author_id>/followers/<path:follower_id>", FollowerDetail.as_view(),
         name="follower_detail"),  # path: allows for forward slashes in arg

]
