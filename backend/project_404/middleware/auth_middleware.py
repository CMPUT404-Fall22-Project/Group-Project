
from authentication.models import Session, ExternalNode
from django.http import HttpResponseBadRequest

skip_paths = ["/swagger", "redoc/"]


class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any([request.path_info.startswith(x) for x in skip_paths]):
            return self.get_response(request)

        request.app_session = None

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
                except:
                    auth_error = HttpResponseBadRequest("Bad token", status=403)
            elif split_auth[0].lower() == "basic":
                try:
                    request.app_session = ExternalNode.objects.get(authorization=auth) # cursed, but passes the check
                except:
                    auth_error = HttpResponseBadRequest("Bad username or password", status=403)

        resp = self.get_response(request)
        if(resp.status_code == 599):
            auth_error["WWW-Authenticate"] = "Basic, Token"
            return auth_error
                

        return resp
