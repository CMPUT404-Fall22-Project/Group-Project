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
from requests import HTTPError


class Ref:
    def __init__(self, data):
        if not "type" in data:
            raise ValueError("Cannot create ref to object with no type")
        if not "id" in data:
            raise ValueError("Cannot create ref to object with no type")

        is_ref = data["type"] == "ref"
        self._ref_data = None
        self._dereferenced = None
        if is_ref:
            self._ref_data = data
        else:
            self._dereferenced = data
            self._ref_data = {"type": "ref", "id": data["id"]}

    def as_ref(self):
        return self._ref_data

    def as_data(self):
        if self._dereferenced != None:
            return self._dereferenced
        result = requests.get(
            self._ref_data["id"],
            headers={'Authorization': get_authorization_from_url(self._ref_data["id"])})
        if result.status_code < 300:
            self._dereferenced = json.loads(result.text)
            return self._dereferenced
        if result.status_code == 404:
            raise Http404(f"Remote server does not have the data. msg={result.text}")
        raise HTTPError(
            f"Unable to dereference remote data. Request returned HTTP{result.status_code}. msg={result.text}")


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
        return get_object_or_404(Author, pk=authorId)

    # looks like we need to contact another server

    result = requests.get(authorString, headers={'Authorization': get_authorization_from_url(authorString)})
    if result.status_code < 300:
        return assign(Author(), json.loads(result.text))

    if result.status_code == 404:
        raise Http404("Remote server returned 404")
    raise BadRequest("Unkown error occured while trying to contact the external server")
