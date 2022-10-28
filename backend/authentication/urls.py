from django.urls import path

from .views import authenticate_user, end_session

# Set up endpoints for CRUD operations
urlpatterns = [
    path("sessions/new/", authenticate_user, name="new_session"),
    path("sessions/end/", end_session, name="end_session"),
    # path("users/<id>", handle_user, name="handle_user"),
]
