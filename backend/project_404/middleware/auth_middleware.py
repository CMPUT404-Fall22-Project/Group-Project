
from authentication.models import Session
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
        auth = None
        token = None
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]

        if auth and auth.startswith("Token "):
            token = auth.split()[1]  # extract token

        if not token:
            allowed = any([request.path_info.startswith(x) for x in allowed_paths])
            if not allowed:
                resp = HttpResponseBadRequest("Missing token", status=401)
                resp["WWW-Authenticate"] = "Token"
                return resp

        if token:
            try:
                sess = Session.objects.get(pk=token)
                request.app_session = sess
            except:
                resp = HttpResponseBadRequest("Bad token", status=403)
                return resp

        return self.get_response(request)
