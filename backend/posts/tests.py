from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from authentication.models import ExternalNode
from authors.models import Author

#NOTE: These tests also tests Likes and comments

class PostTests(APITestCase, URLPatternsTestCase):

    test_post1_data = {"title": "test title",
        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
        "origin":"http://whereitcamefrom.com/posts/zzzzz",
        "description":"This post discusses stuff -- brief",
        "contentType":"text/plain",
        "content":"abc conent 123",
        "published":"2015-03-09T13:07:04Z"}
    
    test_post2_data = {"title": "new",
        "source": "http://newsite.com/posts/yyyyy",
        "origin":"http://newsite.com/posts/zzzzz",
        "description":"new description",
        "contentType":"text/plain",
        "content":"new content",
        "published":"2020-03-09T13:07:04Z"} # new published date
    
    test_comment_data = {"content":"Test content"}
    
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
    
    def get_post_like_list_url(self,author_id,post_id):
        return reverse("post_like_list", args=[author_id, post_id])
    
    def get_comment_list_url(self,author_id,post_id):
        return reverse("comment_list", args=[author_id, post_id])
    
    def get_comment_like_list_url(self,author_id,post_id,comment_id):
        return reverse("comment_like_list", args=[author_id, post_id, comment_id])
    
    def get_liked_list_url(self,author_id):
        return reverse("liked_list", args=[author_id])

    def setUp(self) -> None:
        self.node = ExternalNode(host="http://127.0.0.1:8000/", api="http://127.0.0.1:8000/", authorization="Basic MTVzaXh0ZWVuOjE1c2l4dGVlbg==")
        self.node.save()
        return super().setUp()
    
    
    def post_and_authorize_author(self, author_data):
        """POST author will be tested, but this method prevents redundant code."""
        # post the author
        response = self.client.post(self.get_author_list_url(), author_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
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
        response = self.client.post(self.get_post_list_url(author_id), post_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.data["id"]
        return author_id, post_id
    

    def test_get_posts_for_unauthorized_author(self):
        """Ensure {'type': 'post', 'items': []} is returned for an author with 0 posts."""
        # post an author and get the generated id
        response = self.client.post(self.get_author_list_url(), self.test_author1_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        id = response.data["id"]
        # call get on the posts/ url
        response = self.client.get(self.get_post_list_url(id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_posts_for_authorized_author_with_no_posts(self):
        """Ensure {'type': 'post', 'items': []} is returned for an author with 0 posts."""
        # post an author and get the generated id
        author_id = self.post_and_authorize_author(self.test_author1_data)
        # call get on the posts/ url
        response = self.client.get(self.get_post_list_url(author_id), format='json', HTTP_AUTHORIZATION=self.node.authorization)
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
        response = self.client.post(self.get_post_list_url(author_id), self.test_post1_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
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
        response = self.client.post(self.get_post_list_url(author_id), self.test_post1_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure the post_id is returned
        assert("id" in response.data.keys())
        post_id = response.data["id"]
        # ensure we can retrieve the post from the db
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_post_and_delete_same_post(self):
        """Ensure that a post can be deleted"""
        # post an author, authorize them, post a post and get the generated ids
        author_id, post_id = self.post_a_post(self.test_post1_data)
        # ensure we can retrieve the post by id from the db
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # double-check we are getting the correct id
        data = response.data
        returned_post_id = data["id"].split("posts/")[-1]
        self.assertEqual(returned_post_id, str(post_id))
        # ensure we can delete the post
        response = self.client.delete(self.get_post_detail_url(author_id,post_id), format='json', HTTP_AUTHORIZATION=self.node.authorization)
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
        response = self.client.put(self.get_post_detail_url(author_id,post_id), self.test_post2_data, format='json', HTTP_AUTHORIZATION=self.node.authorization) # send test_post2_data
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get the post to ensure it was properly edited
        response = self.client.get(self.get_post_detail_url(author_id,post_id), format='json')
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_a_post_then_get_all_likes_for_the_post(self):
        """Ensure that an author can like an existing post"""
        # post an author, authorize them, post a post and get the generated ids
        author_id, post_id = self.post_a_post(self.test_post1_data)
        url1 = self.get_post_like_list_url(author_id,post_id)
        # ensure the author can like the post
        response = self.client.post(url1, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # NOTE This must now be done via POST /inbox/
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # # ensure we can get the likes for the post
        # url2 = self.get_post_like_list_url(author_id,post_id)
        # response = self.client.get(url2, format='json')
        # # ensure the proper response code is given
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # # ensure that 1 like was returned for the post
        # data = response.data
        # self.assertEqual(data["type"], "likes")
        # self.assertEqual(len(data["items"]),1)


    def test_add_comment_to_a_post_then_get_all_comments_of_post(self):
        """Ensure 1 comment is returned when we post one comment for a post"""
        # post an author, authorize them, post a post and get the generated ids
        author_id, post_id = self.post_a_post(self.test_post1_data)
        url = self.get_comment_list_url(author_id,post_id)
        # ensure we can get all comments for a post, even when there are none
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper data is returned
        data = response.data
        self.assertEqual(data["type"],"comments")
        self.assertEqual(len(data["items"]),0)

        # ensure the author can POST a comment
        response = self.client.post(url, self.test_comment_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get the comments again
        response = self.client.get(url, format='json')
        # ensure the proper data is returned
        data = response.data
        self.assertEqual(data["type"],"comments")
        self.assertEqual(len(data["items"]),1)

        
    def test_like_a_comment_and_then_get_all_likes_for_the_comment(self):
        """Ensure we can like a comment and successfully return the likes for that comment"""
        # post an author, authorize them, post a post and get the generated ids
        author_id, post_id = self.post_a_post(self.test_post1_data)
        # ensure the author can POST a comment
        url1 = self.get_comment_list_url(author_id,post_id)
        response = self.client.post(url1, self.test_comment_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure we can like the comment
        comment_id = response.data["id"]
        url2 = self.get_comment_like_list_url(author_id,post_id,comment_id)
        response = self.client.post(url2, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ensure there is 1 like for this comment
        response = self.client.get(url2, format='json')
        # ensure the proper response is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure the proper data is depicted
        data = response.data
        self.assertEqual(data["type"],"likes")
        self.assertEqual(len(data["items"]),1)

    def test_like_a_comment_and_like_a_post_then_get_all_likes_for_author(self):
        """Ensure 'liked_list' GET returns 2 likes when we like a post and a comment"""
        # post an author, authorize them, post a post and get the generated ids
        author_id, post_id = self.post_a_post(self.test_post1_data)
        # ensure the author can POST a comment
        url = self.get_comment_list_url(author_id,post_id)
        response = self.client.post(url, self.test_comment_data, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # ensure the proper response code is given
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # NOTE: THE REST OF THIS IS BEING IMPLEMENTED VIA INBOX NOW
        
        # comment_id = response.data["id"]
        # url = self.get_post_like_list_url(author_id,post_id)
        # # ensure the author can like the post
        # response = self.client.post(url, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # print(response,"What do we have here")
        # # ensure the proper response code is given
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # ensure we can like the comment
        # url2 = self.get_comment_like_list_url(author_id,post_id,comment_id)
        # response = self.client.post(url2, format='json', HTTP_AUTHORIZATION=self.node.authorization)
        # # ensure the proper response code is given
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # url = self.get_liked_list_url(author_id)
        # response = self.client.get(url, format='json')
        # # ensure the proper response code is given
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # data = response.data
        # # ensure the proper data was returned
        # self.assertEqual(data["type"],"liked")
        # self.assertEqual(len(data["items"]),2) # 1 for the post and one for the comment