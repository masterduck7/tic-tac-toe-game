import json
import pytest
from rest_framework.test import APIClient

from game.lib.constants import GameConstants
from game.models import Game, User


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
def new_game():
    game = Game.objects.create(
        name="Init",
        status=GameConstants.STATUS_WAITING,
    )
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_one_player(user):
    game = Game.objects.create(
        name="Medium",
        status=GameConstants.STATUS_WAITING,
    )
    game.users.add(user)
    game.save()
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.actual_player = user
    game.save()
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_horizontal(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [user_master.username, user_master.username, 0],
            [0, 0, 0],
            [user.username, user.username, 0],
        ]
    )
    game.save()
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_vertical(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [user_master.username, 0, 0],
            [user_master.username, 0, 0],
            [0, user.username, user.username],
        ]
    )
    game.save()
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_diagonal_1(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [user_master.username, user.username, user.username],
            [0, user_master.username, 0],
            [0, 0, 0],
        ]
    )
    game.save()
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_last_turn_to_win_diagonal_2(user, user_master):
    game = Game.objects.create(
        name="Play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.actual_player = user_master
    game.board = json.dumps(
        [
            [user.username, user.username, user_master.username],
            [0, user_master.username, 0],
            [0, 0, 0],
        ]
    )
    game.save()
    return game
