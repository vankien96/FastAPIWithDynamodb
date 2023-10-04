import random
import string

def random_string(length: int) -> str:
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))