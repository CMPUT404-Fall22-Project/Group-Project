from django.urls import path
from .views import InboxList, InboxDetail, filter_inbox, handle_follow_request, handle_like

urlpatterns = [
    path("authors/<id>/inbox/", InboxList.as_view(), name="inbox_list"),
    path("authors/<id>/inbox", InboxList.as_view(), name="inbox_list"),
    path("authors/<author_id>/inbox/<inbox_id>", InboxDetail.as_view(), name="inbox_detail"),
    path("authors/<author_id>/inbox/filter/", filter_inbox, name="inbox_filter"),
    path("handle-follow-request/", handle_follow_request, name="handle_follow_request"),
    path("handle-like/", handle_like, name="handle_like")
]
