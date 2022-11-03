from django.urls import path
from .views import InboxList, InboxDetail

urlpatterns = [
    path("authors/<id>/inbox/", InboxList.as_view(), name="inbox_list"),
    path("authors/<author_id>/inbox/<inbox_id>", InboxDetail.as_view(), name="inbox_detail")
]