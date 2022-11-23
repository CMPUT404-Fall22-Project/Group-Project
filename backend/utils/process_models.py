from utils.model_utils import get_scheme_and_netloc
from utils.requests import paginate_values
from utils.proxy import fetch_author
from posts.models import Category
from posts.serializers import PostSerializer, CommentSerializer
from authors.serializers import AuthorSerializer


def process_comments(comments):
    parsed = CommentSerializer(comments, many=True).data
    for comment in parsed:
        comment["author"] = AuthorSerializer(fetch_author(comment["author"])).data

    return parsed


def serialize_single_comment(comment):
    return process_comments([comment])[0]

# this method will only be called for posts we own


def process_posts(posts):
    data = []
    if not isinstance(posts, list):
        posts = posts.prefetch_related("author")
    for post in posts:
        serialized = PostSerializer(post).data
        serialized["author"] = AuthorSerializer(post.author).data
        serialized["origin"] = get_scheme_and_netloc() + f"authors/{post.author.id}/posts/{post.id}"
        serialized["source"] = serialized["origin"]
        serialized["id"] = serialized["origin"]

        serialized["categories"] = list(Category.objects.all().filter(post=post).values_list("category", flat=True))

        comments = post.comments.all()
        serialized["comments"] = serialized["origin"] + "/comments"
        serialized["count"] = len(comments)
        serialized["commentsSrc"] = process_comments(paginate_values(0, 5, comments))

        data.append(serialized)

    return data


def serialize_single_post(post):
    return process_posts([post])[0]
