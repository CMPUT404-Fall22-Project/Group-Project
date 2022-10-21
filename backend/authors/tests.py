from http.client import HTTPResponse
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from .models import Author


class AuthorTests(APITestCase, URLPatternsTestCase):

    authors_url = "/authors/"
    test_author_data = {"host":"http://127.0.0.1:5454/",
                        "displayName":"Lara Croft",
                        "github":"http://github.com/laracroft",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    urlpatterns = [
        path('', include('authors.urls')),
    ]


    def test_get_from_empty_database(self):
        """Ensure {'type': 'authors', 'items': []} is returned when no authors are in db."""
        response = self.client.get(self.authors_url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data["type"], "authors")
        self.assertEqual(type(response.data["items"]), list)
        self.assertEqual(len(response.data["items"]), 0) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    def test_post_new_author(self):
        """Ensure an author object can be properly added to the db"""
        url = self.authors_url
        # post the author
        response = self.client.post(url, self.test_author_data, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # get the posted author
        response = self.client.get(self.authors_url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure there is now one author in the db
        self.assertEqual(len(response.data["items"]), 1)
        serialized_author = response.data["items"][0]
        data = dict(serialized_author)

        # ensure all of our keys and values in our post request are contained in the returned author
        for k in self.test_author_data.keys():
            self.assertEqual(data[k], self.test_author_data[k])

        # ensure that all of the proper default values are in the returned author object
        self.assertEqual(data["followers"],[])
        self.assertEqual(data["type"],"author")
        self.assertEqual(data["isAuthorized"],False)
        # ensure that returned id and url follow rubric specs
        self.assertEqual(data["id"],data["url"])
        # ensure that there are no extra keys
        self.assertEqual(len(data.keys()), len(self.test_author_data.keys()) + 5) # 5 keys: "followers", "type", "isAuthorized", "id", "url"