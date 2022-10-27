import random, string

def generate_random_string():
    # e.g. 'PV8dmraVJ5hlVlTPjAix0rmO2QmTOtJ2'
    n=32
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))