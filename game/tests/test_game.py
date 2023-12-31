import json
import pytest
from django.urls import reverse

from game.lib import exceptions as game_exceptions
from game.lib.constants import GameConstants


@pytest.mark.django_db
class TestGameList:
    def setup_method(self):
        self.games_list_url = reverse("game:games-list")

    def test_get_games_list(self, client, game_with_one_player):
        response = client.get(self.games_list_url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == game_with_one_player.name

    def test_get_available_games_list(
        self, client, game_with_one_player, game_with_two_players
    ):
        response = client.get(self.games_list_url, **{"QUERY_STRING": "status=waiting"})

        assert response.status_code == 200
        assert len(response.data) == 1
        for game in response.data:
            assert game["name"] == game_with_one_player.name

    def test_create_game(self, client, user):
        data = {
            "name": "Test a new game",
            "username": user.username,
        }
        response = client.post(self.games_list_url, data)

        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert len(response.data["players"]) == 1
        assert response.data["players"][0]["username"] == data["username"]

    def test_create_game_with_new_user(self, client):
        data = {
            "name": "Test a new game again",
            "username": "A new user",
        }
        response = client.post(self.games_list_url, data)

        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert len(response.data["players"]) == 1
        assert response.data["players"][0]["username"] == data["username"]

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
        assert len(response.data["players"]) == game_with_one_player.players.count()
        assert (
            response.data["players"][0]["username"]
            == game_with_one_player.players.first().username
        )

    def test_get_game_details_raise_game_not_found(self, client):
        url = reverse("game:game-details", kwargs={"name": "false game"})
        response = client.get(url)

        assert response.status_code == 404
        assert (
            response.data["detail"]
            == game_exceptions.GameNotFoundException.default_detail
        )

    def test_update_game(self, client, game_with_one_player, user_master):
        url = reverse("game:game-details", kwargs={"name": game_with_one_player.name})
        data = {
            "name": game_with_one_player.name,
            "username": user_master.username,
        }
        response = client.put(url, data)

        assert response.status_code == 200
        assert response.data["name"] == game_with_one_player.name
        assert len(response.data["players"]) == 2
        assert response.data["status"] == GameConstants.STATUS_IN_GAME
        assert "actual_mark" in response.data
        assert response.data["actual_mark"] == GameConstants.MARK_X

    def test_update_game_raise_full_game_exception(self, client, game_with_two_players):
        url = reverse("game:game-details", kwargs={"name": game_with_two_players.name})
        data = {
            "name": game_with_two_players.name,
            "username": "I want to play",
        }
        response = client.put(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.FullGameStatusException.default_detail
        )

    def test_update_game_raise_serializer_exception(self, client, game_with_one_player):
        url = reverse("game:game-details", kwargs={"name": game_with_one_player.name})
        data = {"name": game_with_one_player.name}
        response = client.put(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.SerializerException.default_detail
        )


@pytest.mark.django_db
class TestPlayGame:
    def test_get_game_details(self, client, game_with_two_players):
        url = reverse("game:play-game", kwargs={"name": game_with_two_players.name})
        response = client.get(url)

        assert response.status_code == 200
        assert response.data["name"] == game_with_two_players.name
        assert len(response.data["players"]) == game_with_two_players.players.count()
        assert "actual_mark" in response.data
        assert response.data["actual_mark"] == GameConstants.MARK_X

    def test_get_game_details_raise_game_not_found(self, client):
        url = reverse("game:play-game", kwargs={"name": "false game"})
        response = client.get(url)

        assert response.status_code == 404
        assert (
            response.data["detail"]
            == game_exceptions.GameNotFoundException.default_detail
        )

    def test_play_game_raise_serializer_exception(self, client, game_with_two_players):
        url = reverse("game:play-game", kwargs={"name": game_with_two_players.name})
        data = {}
        response = client.post(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.SerializerException.default_detail
        )

    def test_play_game_raise_not_valid_status_exception(
        self, client, game_with_one_player
    ):
        url = reverse("game:play-game", kwargs={"name": game_with_one_player.name})
        data = {
            "name": game_with_one_player.name,
            "username": game_with_one_player.players.first().username,
            "movement_x": 0,
            "movement_y": 0,
        }
        response = client.post(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.NotValidGameStatusException.default_detail
        )

    def test_play_game_raise_not_valid_turn_exception(
        self, client, game_with_two_players
    ):
        url = reverse("game:play-game", kwargs={"name": game_with_two_players.name})
        data = {
            "name": game_with_two_players.name,
            "username": game_with_two_players.players.last().username,
            "movement_x": 0,
            "movement_y": 0,
        }
        response = client.post(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.NotUserTurnException.default_detail
        )

    def test_play_game_raise_not_valid_position_exception(
        self, client, game_with_two_players
    ):
        url = reverse("game:play-game", kwargs={"name": game_with_two_players.name})
        data = {
            "name": game_with_two_players.name,
            "username": game_with_two_players.players.first().username,
            "movement_x": 10,
            "movement_y": 10,
        }
        response = client.post(url, data)

        assert response.status_code == 400
        assert (
            response.data["detail"]
            == game_exceptions.NotValidPositionException.default_detail
        )

    def test_play_game_and_not_wins(self, client, game_with_two_players):
        url = reverse("game:play-game", kwargs={"name": game_with_two_players.name})
        data = {
            "name": game_with_two_players.name,
            "username": game_with_two_players.actual_player.username,
            "movement_x": 0,
            "movement_y": 0,
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert response.data["name"] == game_with_two_players.name
        assert response.data["status"] == GameConstants.STATUS_IN_GAME
        assert json.loads(response.data["board"])[0][0] == GameConstants.MARK_X
        assert "actual_mark" in response.data
        assert response.data["actual_mark"] == GameConstants.MARK_O

    def test_play_game_and_wins_horizontal(
        self, client, game_with_two_players_and_last_turn_to_win_horizontal
    ):
        url = reverse(
            "game:play-game",
            kwargs={"name": game_with_two_players_and_last_turn_to_win_horizontal.name},
        )
        data = {
            "name": game_with_two_players_and_last_turn_to_win_horizontal.name,
            "username": game_with_two_players_and_last_turn_to_win_horizontal.actual_player.username,
            "movement_x": 0,
            "movement_y": 2,
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert (
            response.data["name"]
            == game_with_two_players_and_last_turn_to_win_horizontal.name
        )
        assert response.data["status"] == GameConstants.STATUS_FINISHED
        assert response.data["winner"]
        assert (
            response.data["winner"]["username"]
            == game_with_two_players_and_last_turn_to_win_horizontal.actual_player.username
        )

    def test_play_game_and_wins_vertical(
        self,
        client,
        game_with_two_players_and_last_turn_to_win_vertical,
        user_master,
    ):
        url = reverse(
            "game:play-game",
            kwargs={"name": game_with_two_players_and_last_turn_to_win_vertical.name},
        )
        data = {
            "name": game_with_two_players_and_last_turn_to_win_vertical.name,
            "username": user_master.username,
            "movement_x": 2,
            "movement_y": 0,
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert (
            response.data["name"]
            == game_with_two_players_and_last_turn_to_win_vertical.name
        )
        assert response.data["status"] == GameConstants.STATUS_FINISHED
        assert response.data["winner"]
        assert (
            response.data["winner"]["username"]
            == game_with_two_players_and_last_turn_to_win_vertical.actual_player.username
        )

    def test_play_game_and_wins_diagonal_1(
        self,
        client,
        game_with_two_players_and_last_turn_to_win_diagonal_1,
        user_master,
    ):
        url = reverse(
            "game:play-game",
            kwargs={"name": game_with_two_players_and_last_turn_to_win_diagonal_1.name},
        )
        data = {
            "name": game_with_two_players_and_last_turn_to_win_diagonal_1.name,
            "username": user_master.username,
            "movement_x": 2,
            "movement_y": 2,
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert (
            response.data["name"]
            == game_with_two_players_and_last_turn_to_win_diagonal_1.name
        )
        assert response.data["status"] == GameConstants.STATUS_FINISHED
        assert response.data["winner"]
        assert (
            response.data["winner"]["username"]
            == game_with_two_players_and_last_turn_to_win_diagonal_1.actual_player.username
        )

    def test_play_game_and_wins_diagonal_2(
        self,
        client,
        game_with_two_players_and_last_turn_to_win_diagonal_2,
        user_master,
    ):
        url = reverse(
            "game:play-game",
            kwargs={"name": game_with_two_players_and_last_turn_to_win_diagonal_2.name},
        )
        data = {
            "name": game_with_two_players_and_last_turn_to_win_diagonal_2.name,
            "username": user_master.username,
            "movement_x": 2,
            "movement_y": 0,
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert (
            response.data["name"]
            == game_with_two_players_and_last_turn_to_win_diagonal_2.name
        )
        assert response.data["status"] == GameConstants.STATUS_FINISHED
        assert response.data["winner"]
        assert (
            response.data["winner"]["username"]
            == game_with_two_players_and_last_turn_to_win_diagonal_2.actual_player.username
        )
