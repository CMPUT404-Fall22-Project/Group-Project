from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from authors.models import Author
from posts.models import Post
from .models import Inbox
from django.core.exceptions import ValidationError


class InboxTests(APITestCase, URLPatternsTestCase):

    test_author1_data = {"displayName":"Lara Croft",
                        "github":"http://github.com/laracroft",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    test_author2_data = {"displayName":"Spongebob Squarepants",
                        "github":"http://github.com/spongebro",
                        "profileImage":"https://i.imgur.com/k7XVwpB.jpeg"}
    
    test_post1_data = {"title": "test title",
        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
        "origin":"http://whereitcamefrom.com/posts/zzzzz",
        "description":"This post discusses stuff -- brief",
        "contentType":"text/plain",
        "content":"test_content"}
    
    urlpatterns = [
        path('', include('authors.urls')),
        path('', include('inbox.urls')),
        path('', include('posts.urls')),
    ]

    def get_post_list_url(self, id):
        return reverse("post_list", args=[id])
    
    def get_post_detail_url(self,author_id,post_id):
        return reverse("post_detail", args=[author_id, post_id])

    def get_author_list_url(self):
        return reverse("author_list")
    
    def get_author_detail_url(self,id):
        return reverse("author_detail", args=[id])

    def get_inbox_list_url(self,id):
        """id is author.id """
        return reverse("inbox_list", args=[id])
    
    def get_inbox_detail_url(self,author_id,inbox_id):
        return reverse("inbox_detail", args=[author_id,inbox_id])
    

    def post_and_authorize_an_author(self, author_data):
        """POST author will be tested, but this method prevents redundant code."""
        # post the author
        response = self.client.post(self.get_author_list_url(), author_data, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        id = response.data["id"]
        author = get_object_or_404(Author, id=id)
        # authorize the author
        author.isAuthorized = True
        author.save()
        return id
    
    def post_a_post(self, post_data: dict) -> tuple:
        """
        Helper method for adding a post to the db
        Returns (author_id, post_id)
        """
        author_id = self.post_and_authorize_an_author(self.test_author1_data)
        # post the post
        response = self.client.post(self.get_post_list_url(author_id), post_data, format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.data["id"]
        return author_id, post_id

        
    def test_get_inbox_results_for_unauthorized_author(self):
        """Test getting posts for unauthorized author"""
        # post the author (but don't validate)
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json')
        author_id = response.data["id"]
        # get posts from the author's inbox
        response = self.client.get(self.get_inbox_list_url(author_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_all_data_from_empty_inbox_for_authorized_user(self):
        """Test getting posts for an author when there are no posts in inbox"""
        author_id = self.post_and_authorize_an_author(self.test_author1_data)
        # get posts from inbox
        response = self.client.get(self.get_inbox_list_url(author_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the correct data is returned
        keys_arr = ['type', 'author', 'items']
        for key in keys_arr:
            assert(key in list(response.data.keys()))
        self.assertEqual(response.data['type'],"inbox")
        self.assertEqual(response.data['author'],author_id)
        self.assertEqual(len(response.data['items']),0)

        
    def test_post_a_post_and_get_post_from_inbox(self):
        """Test GET from inbox after post is posted"""
        # create an author and get them to post a post
        author_id, post_id = self.post_a_post(self.test_post1_data)
        # get posts from inbox
        response = self.client.get(self.get_inbox_list_url(author_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        inbox_items = response.data['items']
        # ensure there is one inbox_item
        self.assertEqual(len(inbox_items), 1)
        # ensure the inbox post matches the posted post
        for key in self.test_author1_data.keys():
            if key in inbox_items[0].keys():
                self.assertEqual(inbox_items[0][key], self.test_author1_data[key])
    

    def test_send_a_follow_request_and_get_from_inbox(self):
        """Test sending a post to an author's inbox then check the inbox contents"""
        # post an author
        author1_id = self.post_and_authorize_an_author(self.test_author1_data)
        # post another author
        author2_id = self.post_and_authorize_an_author(self.test_author2_data)
        # send a follow request from author2 to author1
        url = self.get_inbox_list_url(author1_id)
        response = self.client.post(url, {"id":author2_id,"type":"follow"}, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get posts from inbox
        response = self.client.get(self.get_inbox_list_url(author1_id), format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper author id is returned
        self.assertEqual(response.data["author"],author1_id)
        # ensure there is 1 item in items
        items = response.data["items"]
        self.assertEqual(len(items),1)

    def test_post_to_and_delete_from_inbox(self):
        """Test posting to and deleting from an author's inbox by id"""
        # post an author
        author1_id = self.post_and_authorize_an_author(self.test_author1_data)
        # post another author
        author2_id = self.post_and_authorize_an_author(self.test_author2_data)
        # send a follow request from author2 to author1
        url = self.get_inbox_list_url(author1_id)
        response = self.client.post(url, {"id":author2_id,"type":"follow"}, format='json')
        inbox_id = response.data["id"]
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get posts from inbox
        response = self.client.get(self.get_inbox_list_url(author1_id), format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper author id is returned
        self.assertEqual(response.data["author"],author1_id)
        # ensure there is 1 item in items
        items = response.data["items"]
        self.assertEqual(len(items),1)
        # ensure we can delete the inbox item
        url = self.get_inbox_detail_url(author1_id,inbox_id)
        response = self.client.delete(url, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the author's inbox is now empty
        response = self.client.get(self.get_inbox_list_url(author1_id), format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper author id is returned
        self.assertEqual(response.data["author"],author1_id)
        # ensure there is 0 item in items
        items = response.data["items"]
        self.assertEqual(len(items),0)


    def test_post_to_and_delete_all_from_inbox(self):
        """Test posting to and deleting from an author's inbox"""
        # post an author
        author1_id = self.post_and_authorize_an_author(self.test_author1_data)
        # post another author
        author2_id = self.post_and_authorize_an_author(self.test_author2_data)
        # send a follow request from author2 to author1
        url = self.get_inbox_list_url(author1_id)
        response = self.client.post(url, {"id":author2_id,"type":"follow"}, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get posts from inbox
        response = self.client.get(self.get_inbox_list_url(author1_id), format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper author id is returned
        self.assertEqual(response.data["author"],author1_id)
        # ensure there is 1 item in items
        items = response.data["items"]
        self.assertEqual(len(items),1)
        # ensure we can delete the inbox item
        url = self.get_inbox_list_url(author1_id)
        response = self.client.delete(url, format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the author's inbox is now empty
        response = self.client.get(self.get_inbox_list_url(author1_id), format='json')
        # ensure the proper response code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper author id is returned
        self.assertEqual(response.data["author"],author1_id)
        # ensure there is 0 item in items
        items = response.data["items"]
        self.assertEqual(len(items),0)