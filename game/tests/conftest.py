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
        status=GameConstants.STATUS_WAITING,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.save()
    return game


@pytest.fixture
@pytest.mark.django_db
def game_with_two_players_and_in_game(user, user_master):
    game = Game.objects.create(
        name="Lets play",
        status=GameConstants.STATUS_IN_GAME,
    )
    game.users.add(user)
    game.users.add(user_master)
    game.save()
    return game
