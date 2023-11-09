import pytest
from django.urls import reverse

from game.lib import exceptions as game_exceptions
from game.lib.constants import GameConstants


@pytest.mark.django_db
class TestGameList:
    def setup_method(self):
        self.games_list_url = reverse("game:games-list")

    def test_get_games_list(self, client, new_game):
        response = client.get(self.games_list_url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == new_game.name

    def test_get_available_games_list(
        self, client, new_game, game_with_two_players_and_in_game
    ):
        response = client.get(self.games_list_url, kwargs={"status": "waiting"})

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["name"] == new_game.name

    def test_create_game(self, client, user):
        data = {
            "name": "Test a new game",
            "username": user.username,
        }
        response = client.post(self.games_list_url, data)

        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert len(response.data["users"]) == 1
        assert response.data["users"][0]["username"] == data["username"]

    def test_create_game_with_new_user(self, client):
        data = {
            "name": "Test a new game again",
            "username": "A new user",
        }
        response = client.post(self.games_list_url, data)

        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert len(response.data["users"]) == 1
        assert response.data["users"][0]["username"] == data["username"]

    def test_create_game_raise_serializer_exception(self, client):
        data = {"name": "Test a new game again"}
        response = client.post(self.games_list_url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.SerializerException.default_detail
        )


@pytest.mark.django_db
class TestGameDetail:
    def test_get_game_details(self, client, game_with_one_player):
        url = reverse("game:game-details", kwargs={"name": game_with_one_player.name})
        response = client.get(url)

        assert response.status_code == 200
        assert response.data["name"] == game_with_one_player.name
        assert len(response.data["users"]) == game_with_one_player.users.count()
        assert (
            response.data["users"][0]["username"]
            == game_with_one_player.users.first().username
        )

    def test_update_game(self, client, game_with_one_player, user_master):
        url = reverse("game:game-details", kwargs={"name": game_with_one_player.name})
        data = {
            "name": game_with_one_player.name,
            "username": user_master.username,
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert response.data["name"] == game_with_one_player.name
        assert len(response.data["users"]) == 2
        assert response.data["status"] == GameConstants.STATUS_IN_GAME

    def test_update_game_raise_full_game_exception(self, client, game_with_two_players):
        url = reverse("game:game-details", kwargs={"name": game_with_two_players.name})
        data = {
            "name": game_with_two_players.name,
            "username": "I want to play",
        }
        response = client.post(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.FullGameStatusException.default_detail
        )

    def test_update_game_raise_serializer_exception(
        self, client, game_with_one_player, user_master
    ):
        url = reverse("game:game-details", kwargs={"name": game_with_one_player.name})
        data = {"name": game_with_one_player.name}
        response = client.post(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.SerializerException.default_detail
        )
