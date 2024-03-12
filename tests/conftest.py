import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from ads.models import Ad, Comment
from users.models import CustomUser

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    return APIClient()


@pytest.fixture
def test_user() -> CustomUser:
    """
    Fixture to provide a test user instance
    :return: CustomUser
    """
    return User.objects.create_user(email="test@example.com", password="@testpassword1")


@pytest.fixture
def test_ad(test_user) -> Ad:
    """
    Fixture to provide an Ad instance
    :param test_user: A User instance
    :return: Ad
    """
    ad = Ad.objects.create(user=test_user, title="title", description="description")
    return ad


@pytest.fixture
def test_ad2() -> Ad:
    """
    Fixture to provide an Ad instance
    :return: Ad
    """
    user = User.objects.create_user(email="test2@example.com", password="@testpassword2")
    ad = Ad.objects.create(user=user, title="title2", description="description2")
    return ad


@pytest.fixture
def test_comment(test_user, test_ad) -> Comment:
    """
    Fixture to provide a comment instance
    :return: Comment
    """
    comment = Comment.objects.create(user=test_user, ad=test_ad, comment_message="comment_message")
    return comment
