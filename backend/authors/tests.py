from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from .models import Author, Follower
from django.core.exceptions import ValidationError


# Follower model is also tested in AuthorTests
class AuthorTests(APITestCase, URLPatternsTestCase):

    test_author1_data = {"displayName":"Lara Croft",
                        "github":"http://github.com/laracroft",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    test_author2_data = {"displayName":"Spongebob Squarepants",
                        "github":"http://github.com/spongebro"}
    
    urlpatterns = [
        path('', include('authors.urls')),
    ]

    def get_author_list_url(self):
        return reverse("author_list")
    
    def get_author_detail_url(self,id):
        return reverse("author_detail", args=[id])
    
    def get_follower_list_url(self, id):
        return reverse("follower_list", args=[id])
    
    def get_follower_detail_url(self,author_id,follower_id):
        return reverse("follower_detail", args=[author_id,follower_id])
    
    def get_following_list_url(self,id):
        return reverse("following_list", args=[id])
    

    def get_full_path_for_test(self, id):
        """ returns str(self.test_author1_data["host"]) + "/authors/" + str(id)"""
        return str("http://127.0.0.1:8000/") + "authors/" + str(id)
    

    def post_and_authorize_author(self, author_data):
        """POST author will be tested, but this method prevents redundant code."""
        # post the author
        response = self.client.post(self.get_author_list_url(), author_data, format='json')
        id = response.data["id"]
        author = get_object_or_404(Author,id=id)
        author.authorize()
        return id




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
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure the id for the posted author was returned
        assert("id" in response.data.keys())
        # ensure id is correct type
        self.assertEqual(type(response.data["id"]), str)

    def test_post_new_author_and_get_all_authors_without_authorizing(self):
        """Ensure a posted author isn't returned after getting all authors"""
        # post the author (but don't authorize them)
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        # get all authors from db
        response = self.client.get(self.get_author_list_url(), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure no authors were returned
        self.assertEqual(len(response.data["items"]), 0)

    def test_post_new_author_and_get_all_authors_after_authorizing(self):
        """Ensure a posted and authorized author is returned after getting all authors"""
        # post and authorize an author and get there id
        id = self.post_and_authorize_author(self.test_author1_data)
        # get all authors from db
        response = self.client.get(self.get_author_list_url(), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure 1 author was returned
        self.assertEqual(len(response.data["items"]), 1)

  
    def test_get_posted_and_authorized_author_by_id(self):
        """Test getting an authorized author by id"""
        # post and authorize an author and get there id
        id = self.post_and_authorize_author(self.test_author1_data)
        url = self.get_author_detail_url(id)
        # try to get the author with specified id
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the data properly corresponds with self.test_author1_data
        for k in self.test_author1_data.keys():
            self.assertEqual(self.test_author1_data[k], response.data[k])
        # ensure "id" is in response.data is in correctly edited format
        #TODO: add this back later
        # correct_id = self.get_full_path_for_test(id)
        # self.assertEqual(correct_id, response.data["id"])
        # ensure url is same as id
        # TODO: fix this later
        # self.assertEqual(response.data["url"], response.data["id"])
        # ensure the author attributes match those of self.test_author1_data
        author = get_object_or_404(Author,id=id)
        for k in self.test_author1_data.keys():
            self.assertEqual(self.test_author1_data[k], getattr(author,k))

    def test_get_uauthorized_author_by_id(self):
        """Test getting an unauthorized author by id"""
        # post the author (but don't authorize them)
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        id = response.data["id"]
        url = self.get_author_detail_url(id)
        # try to get the author with specified id
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_change_author_attributes_via_post(self):
        """
        ensure we can change the attributes of an author
        NOTE: The rubric specfifies handling this operation in POST
        """
        # post an author and get there id
        id = self.post_and_authorize_author(self.test_author1_data)
        url = self.get_author_detail_url(id)
        # ensure we can change the attributes of the author
        response = self.client.post(url, self.test_author2_data, format='json') # using test_author2_data
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get the author whose attributes we changed
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the author now has the attributes of test_author2_data
        data = response.data
        self.assertEqual(data["displayName"], self.test_author2_data["displayName"])
        self.assertEqual(data["github"], self.test_author2_data["github"])
        # ensure profile image is still same ("profileImage" wasn't included in test_author2_data )
        self.assertEqual(data["profileImage"], self.test_author1_data["profileImage"])


        
    def test_get_followers_for_author_with_no_followers(self):
        """Ensure {"type": "followers", "items": []} is returned for author with no followers."""
        # post an author and get there id
        author_id = self.post_and_authorize_author(self.test_author1_data)
        # authorize the author
        author = get_object_or_404(Author, id=author_id)
        author.authorize()
        # get url to enable to get all of this authors followers
        url = self.get_follower_list_url(author_id)
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # assert proper "type" value
        self.assertEqual(response.data["type"], "followers")
        # assert followers size is 0
        self.assertEqual(len(response.data["items"]), 0)

        
    def test_get_followers_for_unauthorized_author(self):
        """Test getting followers for an unauthorized author"""
        # post the author (but don't authorize them)
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        author=get_object_or_404(Author,id=response.data["id"])
        # get url to enable to get all of this authors followers
        url = self.get_follower_list_url(response.data["id"])
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
    def test_add_follower_for_author(self):
        """
        Test that an author is being properly added as follower of another author
        Tested on all four authorization scenarios
        (i.e. both unauthorized, follower unauthorized and author authorized,
        follower authorized and author unauthorized, and both authorized)
        """
        # post the author (but don't authorize them)
        response1 = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        id1 = response1.data["id"]
        # post another author and get there id
        response2 = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        id2 = response2.data["id"]

        # ensure author has no followers to start
        author1 = get_object_or_404(Author, id=id1)
        author2 = get_object_or_404(Author, id=id2)
        followers = author1.followers.all()
        self.assertEqual(len(followers),0)

        # try to PUT author2 as a follower of author1 (author1=unauthorized, author2=unauthorized)
        url = self.get_follower_detail_url(id1, id2)
        response = self.client.put(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try to PUT author2 as a follower of author1 (author1=authorized, author2=unauthorized)
        author1.isAuthorized=True
        author1.save()
        url = self.get_follower_detail_url(id1, id2)
        response = self.client.put(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try to PUT author2 as a follower of author1 (author1=unauthorized, author2=authorized)
        author1.isAuthorized=False
        author1.save()
        author2.isAuthorized=True
        author2.save()
        url = self.get_follower_detail_url(id1, id2)
        response = self.client.put(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

         # try to PUT author2 as a follower of author1 (author1=authorized, author2=authorized)
        author1.isAuthorized=True
        author1.save()
        author2.isAuthorized=True
        author2.save()
        url = self.get_follower_detail_url(id1, id2)
        response = self.client.put(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure author1 now has a follower
        followers = author1.followers.all()
        self.assertEqual(len(followers),1)
        # ensure that author2 is the follower
        author2 = get_object_or_404(Author, id=id2)
        self.assertEqual(followers[0], author2)
        # ensure that author1 is not a follower of author2
        followers = author2.followers.all()
        self.assertEqual(len(followers),0)

        # ensure that Follower now has an entry
        self.assertEqual(len(Follower.objects.all()),1)
        # ensure the follower object has the right data
        follower_obj = Follower.objects.all()[0]
        self.assertEqual(getattr(follower_obj, "author"), author1)
        self.assertEqual(getattr(follower_obj, "follower"), author2)
        self.assertEqual(getattr(follower_obj, "isAccepted"), False)


    def test_set_author_as_follower_of_self(self):
        """Ensure that an author cannot follow themself"""
        # post an author and get there id
        author_id = self.post_and_authorize_author(self.test_author1_data)
        # try to set author as follower of themself
        url = self.get_follower_detail_url(author_id, author_id)
        response = self.client.put(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_an_existing_follower(self):
        # Start by adding one author as a follower of another
        # post an author and get there id
        author1_id = self.post_and_authorize_author(self.test_author1_data)
        # post an author and get there id
        author2_id = self.post_and_authorize_author(self.test_author1_data)
        # ensure author has no followers to start
        author1 = get_object_or_404(Author, id=author1_id)
        followers = author1.followers.all()
        self.assertEqual(len(followers),0)
        # try to PUT author2 as a follower of author1
        url = self.get_follower_detail_url(author1_id, author2_id)
        response = self.client.put(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure author1 now has a follower
        followers = author1.followers.all()
        self.assertEqual(len(followers),1)
        # assert the Follower table now has 1 entry
        self.assertEqual(len(Follower.objects.all()),1)
        # ensure that author2 is the follower
        author2 = get_object_or_404(Author, id=author2_id)
        self.assertEqual(followers[0], author2)
        # delete author2 as a follower of author1
        response = self.client.delete(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure that author1 once again has no followers
        followers = author1.followers.all()
        self.assertEqual(len(followers),0)
        # ensure the Follower table is now empty
        self.assertEqual(len(Follower.objects.all()),0)

    def test_get_all_following_for_author(self):
        """Ensure that the /authors/id/follows/ url returns correct data"""
        # post an author and get there id
        author_id = self.post_and_authorize_author(self.test_author1_data)
        # get all following for this author
        url = self.get_following_list_url(author_id)
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper data is returned
        data = response.data
        self.assertEqual(data["type"],"following")
        self.assertEqual(len(data["items"]),0)
        # post another author and get there id
        follower_id = self.post_and_authorize_author(self.test_author2_data)
        # again get all following for author 1
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper data is returned
        data = response.data
        self.assertEqual(data["type"],"following")
        self.assertEqual(len(data["items"]),0)
        # set author2 as a follower of author1
        url = self.get_follower_detail_url(author_id, follower_id)
        response = self.client.put(url, format='json')
        # get following for follower
        url = self.get_following_list_url(follower_id)
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper data is returned
        data = response.data
        self.assertEqual(data["type"],"following")
        self.assertEqual(len(data["items"]),1)
        # get following for the author
        url = self.get_following_list_url(author_id)
        response = self.client.get(url, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper data is returned
        data = response.data
        self.assertEqual(data["type"],"following")
        self.assertEqual(len(data["items"]),0)

        