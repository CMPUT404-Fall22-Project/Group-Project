
from authentication.models import Session
import datetime


class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.app_session = None
        if not "user_session" in request.COOKIES:
            return self.get_response(request)

        token = request.COOKIES.get("user_session")
        try:
            sess = Session.objects.get(pk=token)
            if not sess.is_expired():
                sess.regenerate_expiry()
                request.app_session = sess
        except:
            pass

        resp = self.get_response(request)
        if request.app_session:
            resp.set_cookie("user_session", request.app_session.token,
                            expires=datetime.datetime.fromtimestamp(request.app_session.expiresAt))

        return resp
