from uuid import uuid4


def uuid():
    """
    Generate a new UUID.
    """
    return uuid4().hex


def uuid6():
    """
    Generate a UUID and truncate it to six characters.
    """
    return uuid()[:6]
