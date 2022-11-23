from django.shortcuts import get_object_or_404
from utils.model_utils import get_scheme_and_netloc
from authors.models import Author
from authentication.models import ExternalNode
from authors.serializers import AuthorSerializer
from django.http import Http404
from django.core.exceptions import BadRequest
import json
import re
import requests


def assign(obj, dict):
    for k, v in dict:
        setattr(obj, k, v)
    return obj


def get_authorization_from_url(url):
    try:
        rootUrl = re.search(r".*?:\/\/.*?\/", url)[0]
        node = ExternalNode.objects.get(pk=rootUrl)
        return node.authorization
    except:
        raise BadRequest("Unable to find authorization details to contact external server")


def fetch_author(data):
    if isinstance(data, Author):
        return data

    # try local first
    try:
        return Author.object.get(pk=data)
    except:
        pass

    # Are we self referrential?
    authorString = data
    if authorString.startswith(get_scheme_and_netloc()):
        authorId = authorString[len(get_scheme_and_netloc() + "authors/"):]
        return get_object_or_404(pk=authorId)

    # looks like we need to contact another server

    result = requests.get(authorString, headers={'Authorization:': get_authorization_from_url(authorString)})
    if result.code == 200:
        return assign(Author(), json.loads(result.text))

    if result.code == 404:
        raise Http404("Remote server returned 404")
    raise BadRequest("Unkown error occured while trying to contact the external server")
