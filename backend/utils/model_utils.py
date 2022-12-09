from project_404 import settings
import uuid


def generate_random_string():
    return uuid.uuid4()


def get_host():
    """Host is either 'http://127.0.0.1:8000/' or 'https://team-sixteen.herokuapp.com/' """
    # if settings.DEBUG:
    #     return 'http://127.0.0.1:8000/'
    return "https://team-sixteen.herokuapp.com/"
