import random
import string
from hashlib import sha256


def get_random_hash(str_size=10):
    allowed_chars = string.ascii_letters + string.punctuation
    random_string = ''.join(random.choice(allowed_chars) for x in range(str_size))
    return sha256(random_string.encode('utf-8')).hexdigest()
