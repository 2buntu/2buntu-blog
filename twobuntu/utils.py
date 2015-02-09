from calendar import timegm
from datetime import datetime
from uuid import uuid4

from django.contrib.auth.models import User
from django.utils.timezone import make_aware, now, utc

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category


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


def timestamp_to_datetime(timestamp):
    """
    Convert a UTC timestamp to a timezone-aware datetime instance.
    """
    return make_aware(datetime.utcfromtimestamp(timestamp), utc)


def datetime_to_timestamp(instance):
    """
    Convert a timezone-aware datetime instance to a UTC timestamp.
    """
    return timegm(instance.utctimetuple())


def dummy_user(staff=False):
    """
    Generate a dummy user for testing.
    """
    if staff:
        return User.objects.create_superuser(
            uuid6(),
            'user@example.com',
            'password',
        )
    else:
        return User.objects.create_user(uuid6())


def dummy_category():
    """
    Generate a dummy category.
    """
    category = Category(name=uuid6())
    category.save()
    return category


def dummy_article(author, category, status):
    """
    Generate a dummy article for testing.
    """
    article = Article(
        author=author,
        category=category,
        title=uuid6(),
        body=uuid6(),
        status=status,
        date=now(),
    )
    article.save()
    return article
