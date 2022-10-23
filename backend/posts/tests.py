from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from .models import Post, Author
from django.core.exceptions import ValidationError



class PostTests(APITestCase, URLPatternsTestCase):

    test_post1_data = {"title": "test title",
        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
        "origin":"http://whereitcamefrom.com/posts/zzzzz",
        "description":"This post discusses stuff -- brief",
        "contentType":"text/plain",
        "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge",
        "published":"2015-03-09T13:07:04Z"}
    
    test_categories = ["web","tutorial"]

    test_author1_data = {"displayName":"Lara Croft",
                        "github":"http://github.com/laracroft",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    test_author2_data = {"displayName":"Spongebob Squarepants",
                        "github":"http://github.com/spongebro",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    urlpatterns = [
        path('', include('authors.urls')),
        path('', include('posts.urls'))

    ]

    def get_author_list_url(self):
        return reverse("author_list")
    
    def get_author_detail_url(self,id):
        return reverse("author_detail", args=[id])
    
    # def get_follower_list_url(self, author_id):
    #     return reverse("follower_list", args=[author_id])
    
    # def get_follower_detail_url(self,author_id,follower_id):
    #     return reverse("follower_detail", args=[author_id,follower_id])
    
    def get_post_list_url(self, id):
        return reverse("post_list", args=[id])
    
    def get_post_detail_url(self,author_id,post_id):
        return reverse("post_detail", args=[author_id, post_id])
    
    
    def post_author(self, author_data: str) -> str:
        """
        Helper method for adding an author to the db
        Returns the id of the posted author
        """
        # post the author
        response = self.client.post(self.get_author_list_url(), author_data, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data["id"]
    
    def post_a_post(self, post_data: dict) -> tuple:
        """
        Helper method for adding a post to the db
        Returns (author_id, post_id)
        """
        author_id = self.post_author(self.test_author1_data)
        # post the post
        response = self.client.post(self.get_post_list_url(author_id), post_data, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.data["id"]
        return author_id, post_id


    def test_get_posts_for_author_with_no_posts(self):
        """Ensure {'type': 'post', 'items': []} is returned for an author with 0 posts."""
        # post an author and get the generated id
        author_id = self.post_author(self.test_author1_data)
        # call get on the posts/ url
        response = self.client.get(self.get_post_list_url(author_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # ensure type key and posts value
        self.assertEqual(response.data["type"], "posts")
        # ensure no items key and no items
        self.assertEqual(len(response.data["items"]), 0)

        
    def test_get_posts_for_author_after_one_post(self):
        """Ensure {'type': 'post', 'items': [<Post>]} is returned for an author with 0 posts."""
        # post an author and get the generated id
        author_id = self.post_author(self.test_author1_data)        
        # ensure we can post a post object for this author
        response = self.client.post(self.get_post_list_url(author_id), self.test_post1_data, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # call get on the posts/ url
        response = self.client.get(self.get_post_list_url(author_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # ensure type key and posts value
        self.assertEqual(response.data["type"], "posts")
        # ensure items key and 1 item
        self.assertEqual(len(response.data["items"]), 1)

        
    def test_post_and_retrieve_a_post_by_id(self):
        """Ensure that the same post we posted is being returned"""
        # post an author and get the generated id
        author_id = self.post_author(self.test_author1_data)
        # ensure we can post a post object for this author
        response = self.client.post(self.get_post_list_url(author_id), self.test_post1_data, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure the post_id is returned
        assert("id" in response.data.keys())
        post_id = response.data["id"]
        # ensure we can retrieve the post from the db
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure self.test_post1_data matches response.data
        for key in self.test_post1_data.keys():
            self.assertEqual(self.test_post1_data[key], response.data[key])

    def test_post_and_delete_same_post(self):
        """Ensure that a post can be deleted"""
        # post an author and get the generated id
        author_id, post_id = self.post_a_post(self.test_post1_data)
        # ensure we can retrieve the post by id from the db
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # double-check we are getting the correct id
        self.assertEqual(response.data["id"], post_id)
        # ensure we can delete the post
        response = self.client.delete(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure we cannot retrieve the deleted post by id from the db
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper 404 response code is now given
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)





    

    # def test_add_follower_for_author(self):
    #     """Test that an author is being properly added as follower of another author"""

    #     # ensure that Follower is initally empty
    #     self.assertEqual(len(Follower.objects.all()),0)
    #     # post an author and get there id
    #     author1_id = self.post_author(self.test_author1_data)
    #     # post another author and get there id
    #     author2_id = self.post_author(self.test_author2_data)
    #     # ensure author has no followers to start
    #     author1 = get_object_or_404(Author, id=author1_id)
    #     followers = author1.followers.all()
    #     self.assertEqual(len(followers),0)

    #     # try to PUT author2 as a follower of author1
    #     url = self.get_follower_detail_url(author1_id, author2_id)
    #     response = self.client.put(url, format='json')
    #     # ensure the proper response code is given
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # ensure author1 now has a follower
    #     followers = author1.followers.all()
    #     self.assertEqual(len(followers),1)
    #     # ensure that author2 is the follower
    #     author2 = get_object_or_404(Author, id=author2_id)
    #     self.assertEqual(followers[0], author2)
    #     # ensure that author1 is not a follower of author2
    #     followers = author2.followers.all()
    #     self.assertEqual(len(followers),0)

    #     # ensure that Follower now has an entry
    #     self.assertEqual(len(Follower.objects.all()),1)
    #     # ensure the follower object has the right data
    #     follower_obj = Follower.objects.all()[0]
    #     self.assertEqual(getattr(follower_obj, "author"), author1)
    #     self.assertEqual(getattr(follower_obj, "follower"), author2)
    #     self.assertEqual(getattr(follower_obj, "isApproved"), False)


    # def test_set_author_as_follower_of_self(self):
    #     """Ensure that an author cannot follow themself"""
    #     # post an author and get there id
    #     author1_id = self.post_author(self.test_author1_data)
    #     # try to set author as follower of themself
    #     url = self.get_follower_detail_url(author1_id, author1_id)
    #     # Should raise validation error
    #     with self.assertRaises(ValidationError):
    #         self.client.put(url, format='json')

    # def test_delete_an_existing_follower(self):
    #     # Start by adding one author as a follower of another
    #     # post an author and get there id
    #     author1_id = self.post_author(self.test_author1_data)
    #     # post another author and get there id
    #     author2_id = self.post_author(self.test_author2_data)
    #     # ensure author has no followers to start
    #     author1 = get_object_or_404(Author, id=author1_id)
    #     followers = author1.followers.all()
    #     self.assertEqual(len(followers),0)
    #     # try to PUT author2 as a follower of author1
    #     url = self.get_follower_detail_url(author1_id, author2_id)
    #     response = self.client.put(url, format='json')
    #     # ensure the proper response code is given
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # ensure author1 now has a follower
    #     followers = author1.followers.all()
    #     self.assertEqual(len(followers),1)
    #     # assert the Follower table now has 1 entry
    #     self.assertEqual(len(Follower.objects.all()),1)
    #     # ensure that author2 is the follower
    #     author2 = get_object_or_404(Author, id=author2_id)
    #     self.assertEqual(followers[0], author2)
    #     # delete author2 as a follower of author1
    #     response = self.client.delete(url, format='json')
    #     # ensure the proper response code is given
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # ensure that author1 once again has no followers
    #     followers = author1.followers.all()
    #     self.assertEqual(len(followers),0)
    #     # ensure the Follower table is now empty
    #     self.assertEqual(len(Follower.objects.all()),0)
        