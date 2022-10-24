from django.db import models
from authors.models import Author
from enum import Enum
from django.shortcuts import get_object_or_404


# Likes, Comments, Public Posts, Friends Only posts, Private posts are all sent to the inbox of the author.
# if the type is “post” then add that post to AUTHOR_ID’s inbox
# if the type is “follow” then add that follow to AUTHOR_ID’s inbox to approve later
# if the type is “like” then add that like to AUTHOR_ID’s inbox
# if the type is “comment” then add that comment to AUTHOR_ID’s inbox

class Inbox(models.Model):

    class DataType(Enum):
        POST = "post"
        FOLLOW = "follow"
        LIKE = "like"
        COMMENT = "comment"

    type = models.CharField(max_length=255, default="inbox", editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    data = models.JSONField(null=True) # https://www.youtube.com/watch?v=LbdUpY1I1zg&t=789s&ab_channel=PrettyPrinted

    
    def __str__(self):
        """Returns the displayName of the inbox's Author"""
        return self.author.displayName
    
    def get_data(self, data_type: DataType = None):
        """
        Returns all of the posts from the inbox by self.DataType.data_type.
        If data_type argument is not included, then all data is returned.
        """
        if data_type:
            return self.data[data_type]
        return self.data