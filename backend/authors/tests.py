from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from .models import Author


class AuthorTests(APITestCase, URLPatternsTestCase):

    test_author_data = {"host":"http://127.0.0.1:5454/",
                        "displayName":"Lara Croft",
                        "github":"http://github.com/laracroft",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    urlpatterns = [
        path('', include('authors.urls')),
    ]

    def get_author_list_url(self):
        return reverse("author_list")
    
    def get_author_detail_url(self,id):
        return reverse("author_detail", args=[id])

    
    def get_full_path_for_test(self, id):
        """ returns str(self.test_author_data["host"]) + "/authors/" + str(id)"""
        return str(self.test_author_data["host"]) + "authors/" + str(id)
    

    def test_get_from_empty_database(self):
        """Ensure {'type': 'authors', 'items': []} is returned when no authors are in db."""
        response = self.client.get(self.get_author_list_url(), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data["type"], "authors")
        self.assertEqual(type(response.data["items"]), list)
        self.assertEqual(len(response.data["items"]), 0)

        
    def test_post_new_author(self):
        """Ensure an author object is properly added to the db"""
        # post the author
        response = self.client.post(self.get_author_list_url(), self.test_author_data, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure the id for the posted author was returned
        assert("id" in response.data.keys())
        # ensure id is correct type
        self.assertEqual(type(response.data["id"]), str)
        # get all authors from db
        response = self.client.get(self.get_author_list_url(), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure there is now one author in the db
        self.assertEqual(len(response.data["items"]), 1)

  
    def test_get_posted_author_by_id(self):
        # post the author
        response = self.client.post(self.get_author_list_url(), self.test_author_data, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure the id for the posted author was returned
        assert("id" in response.data.keys())
        id = response.data["id"]
        url = self.get_author_detail_url(id)
        # try to get the author with specified id
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # ensure the data properly corresponds with self.test_author_data
        for k in self.test_author_data.keys():
            self.assertEqual(self.test_author_data[k], response.data[k])
        # ensure "id" is in response.data is in correctly edited format
        correct_id = self.get_full_path_for_test(id)
        self.assertEqual(correct_id, response.data["id"])
        # ensure url is same as id
        self.assertEqual(response.data["url"], response.data["id"])

        # assert the object with id==id now exists
        assert((type(get_object_or_404(Author, id=id)) == Author))
        # get the existing object
        author = get_object_or_404(Author, id=id)
        # ensure the attributes match those of self.test_author_data
        for k in self.test_author_data.keys():
            self.assertEqual(self.test_author_data[k], getattr(author,k))







    #     serialized_author = response.data["items"][0]
    #     data = dict(serialized_author)

    #     # ensure all of our keys and values in our post request are contained in the returned author data
    #     for k in self.test_author_data.keys():
    #         self.assertEqual(data[k], self.test_author_data[k])

    #     # ensure that all of the proper default values are in the returned author object
    #     self.assertEqual(data["followers"],[])
    #     self.assertEqual(data["type"],"author")
    #     self.assertEqual(data["isAuthorized"],False)
    #     # ensure id and url are identical
    #     self.assertEqual(data["id"], data["url"])
    #     # ensure that the returned id and url follow the get_full_path() structure
    #     correct_id = self.get_full_path_for_test(id)
    #     self.assertEqual(correct_id, data["id"])
    #     self.assertEqual(correct_id, data["url"])
    #     # ensure that there are no extra keys
    #     self.assertEqual(len(data.keys()), len(self.test_author_data.keys()) + 5) # 5 keys: "followers", "type", "isAuthorized", "id", "url"