from django.db import models
from authors.models import Author


# Likes, Comments, Public Posts, Friends Only posts, Private posts are all sent to the inbox of the author.
# if the type is “post” then add that post to AUTHOR_ID’s inbox
# if the type is “follow” then add that follow to AUTHOR_ID’s inbox to approve later
# if the type is “like” then add that like to AUTHOR_ID’s inbox
# if the type is “comment” then add that comment to AUTHOR_ID’s inbox


class Inbox(models.Model):

    POST = "post"
    FOLLOW = "follow"
    LIKE = "like"
    COMMENT = "comment"
    CHOICES = [(POST,POST),(FOLLOW,FOLLOW),(LIKE,LIKE),(COMMENT,COMMENT)]

    type = models.CharField(max_length=5, default="inbox", editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="inboxes")
    dataType = models.CharField(choices=CHOICES, max_length=7)
    data = models.JSONField() # https://www.youtube.com/watch?v=LbdUpY1I1zg&t=789s&ab_channel=PrettyPrinted

    
    def __str__(self):
        """Returns the displayName of the inbox's Author"""
        return self.author.displayName

        
    def set_data_and_dataType(self,data):
        """
        Sets self.dataType=data.type, self.data=data, and then saves
        @params - data: a Post, Follow, Like, or Comment
        """
        self.dataType = data.type
        self.data = data
        self.save()