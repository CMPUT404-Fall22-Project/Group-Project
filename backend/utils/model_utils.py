import random
import string


def generate_random_string():
    # e.g. 'PV8dmraVJ5hlVlTPjAix0rmO2QmTOtJ2'
    n = 32
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def get_scheme_and_netloc():
    """TODO: This needs to include scheme and netloc"""
    return 'http://127.0.0.1:8000/'
