from django.urls import path

from .views import authenticate_user, end_session, user_exists, signup

# Set up endpoints for CRUD operations
urlpatterns = [
    path("sessions/new/", authenticate_user, name="new_session"),
    path("sessions/end/", end_session, name="end_session"),
    path("users/check/<id>/", user_exists, name="check_user_exists"),
    path("users/signup/", signup, name="check_user_exists"),
]
