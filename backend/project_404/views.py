from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseBadRequest
from utils.proxy import get_authorization_from_url
from utils.requests import get_parameter_or_default
import requests


@api_view(["GET", "POST"])
def proxy_request(request):
    """
    URL: ://service/proxy/

    Searches the inbox and returns the 
    params:
        PROXY_TARGET: the target of the proxy
        ... args
    """
    proxy_target = get_parameter_or_default(request, "PROXY_TARGET", None)
    if not proxy_target:
        return HttpResponseBadRequest("Missing required field 'PROXY_TARGET'")
    
    params = request.GET.copy()
    del params["PROXY_TARGET"]

    auth = get_authorization_from_url(proxy_target)

    if request.method == "GET":
        response = requests.get(proxy_target, params=params, headers={'Authorization': auth})
        if response.status_code > 201:
            return HttpResponseBadRequest(f"Error attempting to proxy GET request to destination server '{proxy_target}' -- HTTP{response.status_code}: {response.text}", status=502)
        return JsonResponse(response.json(), safe=False)
    
    # post
    response = requests.get(proxy_target, data=request.POST, headers={'Authorization': auth})
    if response.status_code > 201:
        return HttpResponseBadRequest(f"Error attempting to proxy POST request to destination server '{proxy_target}' -- HTTP{response.status_code}: {response.text}", status=502)
    return JsonResponse(response.json(), safe=False)
