
from authentication.models import Session, ExternalNode
from django.http import HttpResponseBadRequest

skip_paths = ["/swagger", "redoc/"]

allowed_paths = ["/sessions/", "/users/", "/admin/"]


class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any([request.path_info.startswith(x) for x in skip_paths]):
            return self.get_response(request)

        request.app_session = None

        authorized = False
        auth_error = HttpResponseBadRequest("Unauthorized", status=401)
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            split_auth = auth.split()
            if len(split_auth) < 2:
                auth_error = HttpResponseBadRequest("Malformed Authroization header. Expecting BASIC xxx or TOKEN xxx", status=403)
            elif split_auth[0].lower() == "token":
                token = split_auth[1]  # extract token
                try:
                    sess = Session.objects.get(pk=token)
                    request.app_session = sess
                    authorized = True
                except:
                    auth_error = HttpResponseBadRequest("Bad token", status=403)
            elif split_auth[0].lower() == "basic":
                user_pass = split_auth[1]
                try:
                    ExternalNode.object.get(authorization=user_pass)
                    authorized = True
                except:
                    auth_error = HttpResponseBadRequest("Bad username or password", status=403)

        if not authorized:
            allowed = any([request.path_info.startswith(x) for x in allowed_paths])
            if not allowed:
                resp = auth_error
                resp["WWW-Authenticate"] = "Basic, Token"
                return resp

        return self.get_response(request)
