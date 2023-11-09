import pytest


@pytest.mark.django_db
class TestGame:
    def test_game_str(self, new_game):
        assert str(new_game) == new_game.name


@pytest.mark.django_db
class TestUser:
    def test_user_str(self, user):
        assert str(user) == user.username
