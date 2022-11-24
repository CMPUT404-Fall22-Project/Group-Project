import random
import string
from project_404 import settings


def generate_random_string():
    # e.g. 'PV8dmraVJ5hlVlTPjAix0rmO2QmTOtJ2'
    n = 32
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def get_host():
    """Host is either 'http://127.0.0.1:8000/' or 'https://team-sixteen.herokuapp.com/' """
    if settings.DEBUG:
        return 'http://127.0.0.1:8000/'
    return "https://team-sixteen.herokuapp.com/"