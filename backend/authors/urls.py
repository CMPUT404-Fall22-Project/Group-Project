from django.urls import path
from . import views

# Set up endpoints for CRUD operations
urlpatterns = [
    path("authors/", views.AuthorList.as_view()),
    path("authors/<pk>/", views.AuthorDetail.as_view()),
]