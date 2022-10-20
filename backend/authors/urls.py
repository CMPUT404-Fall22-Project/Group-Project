from django.urls import path

from . import views

# Set up endpoints for CRUD operations
urlpatterns = [
    path("authors/", views.AuthorList.as_view()),
    path("authors/<id>/", views.AuthorDetail.as_view()),
    path("authors/<id>/followers/", views.FollowerList.as_view()),
    path("authors/<author_id>/followers/<follower_id>", views.FollowerDetail.as_view())
]