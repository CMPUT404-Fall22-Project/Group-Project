from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from authors.models import Author


class PostTests(APITestCase, URLPatternsTestCase):

    test_post1_data = {"title": "test title",
        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
        "origin":"http://whereitcamefrom.com/posts/zzzzz",
        "description":"This post discusses stuff -- brief",
        "contentType":"text/plain",
        "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge",
        "published":"2015-03-09T13:07:04Z"}
    
    test_post2_data = {"title": "new",
        "source": "http://newsite.com/posts/yyyyy",
        "origin":"http://newsite.com/posts/zzzzz",
        "description":"new description",
        "contentType":"text/plain",
        "content":"new content",
        "published":"2020-03-09T13:07:04Z"} # new published date
    
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
    
    
    def post_and_authorize_author(self, author_data):
        """POST author will be tested, but this method prevents redundant code."""
        # post the author
        response = self.client.post(self.get_author_list_url(), author_data, format='json')
        id = response.data["id"]
        author = get_object_or_404(Author,id=id)
        author.authorize()
        return id
    
    def post_a_post(self, post_data: dict) -> tuple:
        """
        Helper method for adding a post to the db
        Returns (author_id, post_id)
        """
        author_id = self.post_and_authorize_author(self.test_author1_data)
        # post the post
        response = self.client.post(self.get_post_list_url(author_id), post_data, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.data["id"]
        return author_id, post_id
    

    def test_get_posts_for_unauthorized_author(self):
        """Ensure {'type': 'post', 'items': []} is returned for an author with 0 posts."""
        # post an author and get the generated id
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        id = response.data["id"]
        # call get on the posts/ url
        response = self.client.get(self.get_post_list_url(id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_posts_for_authorized_author_with_no_posts(self):
        """Ensure {'type': 'post', 'items': []} is returned for an author with 0 posts."""
        # post an author and get the generated id
        author_id = self.post_and_authorize_author(self.test_author1_data)
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
        author_id = self.post_and_authorize_author(self.test_author1_data)       
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
        author_id = self.post_and_authorize_author(self.test_author1_data) 
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
        # post an author, authorize them, post a post and get the generated ids
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

    def test_put_a_post(self):
        """Ensure that a post can be edited"""
        # post an author, authorize them, post a post and get the generated ids
        author_id, post_id = self.post_a_post(self.test_post1_data)
        # ensure we can edit the post
        response = self.client.put(self.get_post_detail_url(author_id,post_id), self.test_post2_data, format='json') # send test_post2_data
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get the post to ensure it was properly edited
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure that the 'putted' post now matches the data we used to edit with
        post = response.data
        for key in self.test_post2_data.keys():
            self.assertEqual(post[key], self.test_post2_data[key])




