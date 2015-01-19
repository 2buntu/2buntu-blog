from uuid import uuid4

from django.contrib.auth.models import User
from django.utils.timezone import now

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


def dummy_article(author, category, status=Article.PUBLISHED):
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
