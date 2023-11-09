import pytest
from django.urls import reverse

from game.lib import exceptions as game_exceptions


@pytest.mark.django_db
class TestUserDetail:
    def test_get_user_details(self, client, user):
        url = reverse("game:user-details", kwargs={"username": user.username})
        response = client.get(url)

        assert response.status_code == 200
        assert "games" in response.data
        assert "user" in response.data
        assert len(response.data["games"]) == 0
        assert response.data["user"]["username"] == user.username

    def test_get_user_details_raise_user_not_found(self, client):
        url = reverse("game:user-details", kwargs={"username": "false user"})
        response = client.get(url)

        assert response.status_code == 404
        assert "games" not in response.data
        assert "user" not in response.data


@pytest.mark.django_db
class TestUserList:
    def setup_method(self):
        self.user_list_url = reverse("game:user-list")

    def test_create_user(self, client):
        data = {"username": "A new user want to play"}
        response = client.post(self.user_list_url, data)

        assert response.status_code == 201
        assert response.data["username"] == data["username"]

    def test_create_user_raise_serializer_exception(self, client):
        data = {"wrong_field": "A new user want to play"}
        response = client.post(self.user_list_url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.SerializerException.default_detail
        )
