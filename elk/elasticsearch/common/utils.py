import random
import string


def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_measurements(timestamp):
    """

    Args:
        timestamp:

    Returns:

    """
    return []