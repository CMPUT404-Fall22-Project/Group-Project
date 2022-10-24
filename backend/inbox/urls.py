from django.urls import path
from .views import InboxList


urlpatterns = [
    path("authors/<id>/inbox", InboxList.as_view(), name="inbox_list"),
]