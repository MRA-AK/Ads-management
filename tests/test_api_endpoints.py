import pytest
from django.urls import reverse

from ads.models import Ad, Comment


@pytest.mark.django_db
class TestAds:
    """Test ads endpoints"""

    def test_create_ad_unauthorized(self, api_client) -> None:
        """
        Test creatign a new ad with authorizated user

        :param api_client: APIClient object to send the request
        :return: None
        """

        url = reverse("ad-list")
        response = api_client.post(url, data={}, format="json")
        assert response.status_code == 401

    def test_create_ad_authorized_wrong_payload(self, api_client, test_user) -> None:
        """
        Test creatign a new ad with wrong payload

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :return: None
        """

        api_client.force_authenticate(test_user)
        url = reverse("ad-list")
        response = api_client.post(url, data={}, format="json")
        assert response.status_code == 400

    def test_create_ad_authorized(self, api_client, test_user) -> None:
        """
        Test creatign a new ad with authorized user and valid data

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :return: None
        """

        payload = {"title": "Test Ad", "description": "This is test ad"}

        api_client.force_authenticate(test_user)
        url = reverse("ad-list")
        response = api_client.post(url, data=payload, format="json")

        ad = Ad.objects.last()

        assert response.status_code == 201
        assert Ad.objects.count() == 1
        assert ad.title == payload["title"]
        assert ad.description == payload["description"]
        assert ad.user == test_user

    def test_get_ad_authorized(self, api_client, test_ad) -> None:
        """
        Test get a list of ads with unauthorized user

        :param api_client: APIClient object to send the request
        :param test_ad: Ad instance
        :return: None
        """

        url = reverse("ad-list")
        response = api_client.get(url)

        assert response.status_code == 200
        print()
        assert response.json()["count"] == 1
        assert len(response.json()["results"]) == 1

    def test_update_ad(self, api_client, test_user, test_ad) -> None:
        """
        Test updating ad wiht authorized user

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :param test_ad: A created test ad
        :return: None
        """

        payload = {"title": "New title"}

        api_client.force_authenticate(test_user)
        url = reverse("ad-detail", kwargs={"pk": test_ad.pk})
        response = api_client.patch(url, data=payload, format="json")

        ad = Ad.objects.last()

        assert response.status_code == 200
        assert Ad.objects.count() == 1
        assert ad.title == payload["title"]

    def test_update_someone_else_ad(self, api_client, test_user, test_ad2) -> None:
        """
        Test updating someone else ads (created by other user)

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :param test_ad2: A created test ad
        :return: None
        """

        payload = {"title": "New title"}

        api_client.force_authenticate(test_user)
        url = reverse("ad-detail", kwargs={"pk": test_ad2.pk})
        response = api_client.patch(url, data=payload, format="json")
        assert response.status_code == 404

    def test_delete_ad(self, api_client, test_user, test_ad) -> None:
        """
        Test updating ad wiht authorized user

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :param test_ad: A created test ad
        :return: None
        """

        api_client.force_authenticate(test_user)
        url = reverse("ad-detail", kwargs={"pk": test_ad.pk})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Ad.objects.count() == 0

    def test_delete_someone_else_ad(self, api_client, test_user, test_ad2) -> None:
        """
        Test deleting someone else ads (created by other user)

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :param test_ad2: A created test ad
        :return: None
        """
        api_client.force_authenticate(test_user)
        url = reverse("ad-detail", kwargs={"pk": test_ad2.pk})
        response = api_client.delete(url)

        assert response.status_code == 404
        assert Ad.objects.count() == 1


@pytest.mark.django_db
class TestComments:
    """Test comments endpoints"""

    def test_create_comment_unauthorized(self, api_client) -> None:
        """
        Test creatign a new comment with authorizated user

        :param api_client: APIClient object to send the request
        :return: None
        """

        url = reverse("create_comment")
        response = api_client.post(url, data={}, format="json")
        assert response.status_code == 401

    def test_create_comment_authorized_wrong_payload(self, api_client, test_user) -> None:
        """
        Test creatign a new comment with wrong payload

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :return: None
        """

        api_client.force_authenticate(test_user)
        url = reverse("create_comment")
        response = api_client.post(url, data={}, format="json")
        assert response.status_code == 400

    def test_create_comment_authorized(self, api_client, test_user, test_ad) -> None:
        """
        Test creatign a new comment with authorized user and valid data

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :param test_ad: A created test ad
        :return: None
        """

        payload = {"comment_message": "This is a comment", "ad": test_ad.pk}

        api_client.force_authenticate(test_user)
        url = reverse("create_comment")
        response = api_client.post(url, data=payload, format="json")

        comment = Comment.objects.last()

        assert response.status_code == 201
        assert Comment.objects.count() == 1
        assert comment.comment_message == payload["comment_message"]
        assert comment.user == test_user
        assert comment.ad == test_ad

    def test_create_duplicate_comment_authorized(self, api_client, test_user, test_ad, test_comment) -> None:
        """
        Test creatign duplicate comment with authorized user and valid data

        :param api_client: APIClient object to send the request
        :param test_user: User object
        :param test_ad: A created test ad
        :param test_comment: A created comment
        :return: None
        """

        payload = {"comment_message": "This is a second comment", "ad": test_ad.pk}

        api_client.force_authenticate(test_user)
        url = reverse("create_comment")
        response = api_client.post(url, data=payload, format="json")

        assert response.status_code == 400
        assert Comment.objects.count() == 1
