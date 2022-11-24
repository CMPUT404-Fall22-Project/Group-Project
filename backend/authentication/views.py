from authors.serializers import AuthorSerializer
from utils.requests import get_parameter_or_default
from utils.requests import get_any_parameter_or_default
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.db import transaction

from .models import Session, User
import hashlib
import secrets
import base64


def gen_random_salt():
    return secrets.token_hex(16)


def hash_passwd(passwd, salt):
    return str(base64.b64encode(hashlib.scrypt(bytes(passwd, "utf-8"), salt=bytes(salt, "utf-8"), n=16, r=1, p=1)))


@api_view(["POST"])
def authenticate_user(request):

    invalid_credentials_string = "Incorrect username or password."

    username = get_parameter_or_default(request, "username", None, use_post=True)
    password = get_parameter_or_default(request, "password", None, use_post=True)

    if not username or not password:
        return HttpResponse("Missing username or password", status=400)

    try:
        user = User.objects.get(pk=username)
    except User.DoesNotExist:
        return HttpResponse(invalid_credentials_string, status=401)

    salt = user.salt

    hashed = hash_passwd(password, salt)

    if hashed != user.passwordHash:
        return HttpResponse(invalid_credentials_string, status=401)

    # check if the user is authorized or not. if not, send back a 403 forbidden
    if not user.author.isAuthorized:
        return HttpResponse("Account not yet authorized by server admin.", status=403)

    session = Session.objects.get(user=user)
    resp = JsonResponse({"token": session.token, "author": AuthorSerializer(user.author).data}, safe=False)
    return resp


def user_exists_db(id):
    try:
        User.objects.get(pk=id)
        return True
    except User.DoesNotExist:
        return False


@api_view(["GET"])
def user_exists(request, id):
    return JsonResponse({"value": user_exists_db(id)}, safe=False)


@api_view(["POST"])
@transaction.atomic
def signup(request):
    author_data = get_any_parameter_or_default(request, "author_data", None, use_post=True)
    user_data = get_any_parameter_or_default(request, "user_data", None, use_post=True)

    if not author_data or not user_data:
        return HttpResponseBadRequest("Missing author or user field.")

    serializer = AuthorSerializer(data=author_data)
    if serializer.is_valid():
        author = serializer.save()
    else:
        return HttpResponseBadRequest("Malformed author field. " + str(serializer.errors))

    if not "password" in user_data or not "username" in user_data:
        return HttpResponseBadRequest("Malformed user field.")

    if user_exists_db(user_data["username"]):
        return HttpResponseBadRequest("User already exists.")

    salt = gen_random_salt()
    hashed = hash_passwd(user_data["password"], salt)

    user = User(username=user_data["username"], passwordHash=hashed, salt=salt, author=author)
    user.save()
    # looks good, give them a session back
    session_token = secrets.token_urlsafe(32)
    # save CCID as it is a high access field
    session = Session(user=user, author=user.author, token=session_token)
    session.save()
    return HttpResponse(status=201)
