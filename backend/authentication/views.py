from http.client import HTTPResponse
from authors.serializers import AuthorSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse

from .models import Session, User
import hashlib
import secrets
import base64
import time


def clear_ended_sessions():
    t = int(time.time() * 1000)
    for obj in Session.objects.filter(expires_at__lt=t):
        obj.delete()


@api_view(["GET"])
def authenticate_user(request):

    bad_auth_field_str = "Bad authorization field in request."
    invalid_credentials_string = "Incorrect username or password."

    if not "Authorization" in request.headers:
        return JsonResponse({"error": "Missing username or password"}, status=400, safe=False)

    auth = request.headers["Authorization"]

    if not auth.startswith("basic "):
        return JsonResponse({"error": bad_auth_field_str}, status=400, safe=False)

    auth = auth[6:].split(":")
    if len(auth) != 2:
        return JsonResponse({"error": bad_auth_field_str}, status=400, safe=False)

    username = base64.b64decode(auth[0])
    passwd = base64.b64decode(auth[1])

    try:
        user = User.objects.get(pk=username)
    except User.DoesNotExist:
        return JsonResponse({"error": invalid_credentials_string}, status=401, safe=False)

    salt = user.salt

    hashed = str(base64.b64encode(hashlib.scrypt(bytes(passwd, "utf-8"), salt=bytes(salt, "utf-8"), n=16, r=1, p=1)))

    if hashed != user.passwordHash:
        return JsonResponse({"error": invalid_credentials_string}, status=401, safe=False)

    # looks good, give them a session back
    session_token = secrets.token_urlsafe(32)
    # save CCID as it is a high access field
    session = Session(user=user, author=user.author, token=session_token)
    session.regenerate_expiry()

    # delete all lingering sessions
    clear_ended_sessions()

    resp = JsonResponse({"token": session_token, "author": AuthorSerializer(user.author)}, safe=False)
    resp.set_cookie("user_session", session.token, expires=session.expiresAt)

    return resp


@api_view(["GET"])
def end_session(request):

    if not request.app_session:
        return HTTPResponse(status=200)  # not logged in, but OK

    try:
        request.app_session.delete()
        return HTTPResponse(status=200)
    except:
        return HTTPResponse("Session could not be ended", status=500)
