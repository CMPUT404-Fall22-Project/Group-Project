from django.http import HttpResponseBadRequest
from rest_framework.request import Request

def authenticated(func):

    def wrapper(*args, **kwargs):
        try:
            for arg in args:
                if isinstance(arg, Request):
                    if arg.app_session:
                        return func(*args, **kwargs)
                    else:
                        return HttpResponseBadRequest(status=599)
        except:
            pass
        return HttpResponseBadRequest(status=599)

    return wrapper
