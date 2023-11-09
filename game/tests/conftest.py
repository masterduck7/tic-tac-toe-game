import json
import pytest
from rest_framework.test import APIClient

from game.lib.constants import GameConstants
from game.models import Game, User, UserGame


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def user():
    user = User.objects.create(username="Jerry")
    return user


@pytest.fixture
@pytest.mark.django_db
def user_master():
    user = User.objects.create(
        username="Tom",
        number_of_games=10,
        points=10,
    )
    return user


@pytest.fixture
@pytest.mark.django_db
def game_with_one_player(user):
    game = Game.objects.create(
        name="Medium",
        status=GameConstants.STATUS_WAITING,
    )
    game.players.add(user)
    game.save()

    user_game = UserGame.objects.get(user=user, game=game)
    user_game.character = GameConstants.CHARACTERS_X
    user_game.save()

    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.players.add(user)
    game.players.add(user_master)
    game.actual_player = user
    game.save()

    user_game = UserGame.objects.get(user=user, game=game)
    user_game.character = GameConstants.CHARACTERS_X
    user_game.save()
    user_master_game = UserGame.objects.get(user=user_master, game=game)
    user_master_game.character = GameConstants.CHARACTERS_O
    user_master_game.save()

    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_horizontal(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.players.add(user)
    game.players.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [GameConstants.CHARACTERS_O, GameConstants.CHARACTERS_O, ""],
            ["", "", ""],
            [GameConstants.CHARACTERS_X, GameConstants.CHARACTERS_X, ""],
        ]
    )
    game.save()

    user_game = UserGame.objects.get(user=user, game=game)
    user_game.character = GameConstants.CHARACTERS_X
    user_game.save()
    user_master_game = UserGame.objects.get(user=user_master, game=game)
    user_master_game.character = GameConstants.CHARACTERS_O
    user_master_game.save()

    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_vertical(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.players.add(user)
    game.players.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [GameConstants.CHARACTERS_O, "", ""],
            [GameConstants.CHARACTERS_O, "", ""],
            ["", GameConstants.CHARACTERS_X, GameConstants.CHARACTERS_X],
        ]
    )
    game.save()

    user_game = UserGame.objects.get(user=user, game=game)
    user_game.character = GameConstants.CHARACTERS_X
    user_game.save()
    user_master_game = UserGame.objects.get(user=user_master, game=game)
    user_master_game.character = GameConstants.CHARACTERS_O
    user_master_game.save()

    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_diagonal_1(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.players.add(user)
    game.players.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [
                GameConstants.CHARACTERS_O,
                GameConstants.CHARACTERS_X,
                GameConstants.CHARACTERS_X,
            ],
            ["", GameConstants.CHARACTERS_O, ""],
            ["", "", ""],
        ]
    )
    game.save()

    user_game = UserGame.objects.get(user=user, game=game)
    user_game.character = GameConstants.CHARACTERS_X
    user_game.save()
    user_master_game = UserGame.objects.get(user=user_master, game=game)
    user_master_game.character = GameConstants.CHARACTERS_O
    user_master_game.save()

    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_diagonal_2(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.players.add(user)
    game.players.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [
                GameConstants.CHARACTERS_X,
                GameConstants.CHARACTERS_X,
                GameConstants.CHARACTERS_O,
            ],
            ["", GameConstants.CHARACTERS_O, ""],
            ["", "", ""],
        ]
    )
    game.save()

    user_game = UserGame.objects.get(user=user, game=game)
    user_game.character = GameConstants.CHARACTERS_X
    user_game.save()
    user_master_game = UserGame.objects.get(user=user_master, game=game)
    user_master_game.character = GameConstants.CHARACTERS_O
    user_master_game.save()

    return game
