import pytest


@pytest.mark.django_db
class TestGame:
    def test_game_str(self, game_with_one_player):
        assert str(game_with_one_player) == game_with_one_player.name


@pytest.mark.django_db
class TestUser:
    def test_user_str(self, user):
        assert str(user) == user.username
