from django.urls import path

from game.views import game, user

app_name = "game"

urlpatterns = [
    path("games/", game.GamesList.as_view(), name="games-list"),
    path("games/<str:name>/", game.GameDetail.as_view(), name="game-details"),
    path("games/<str:name>/play/", game.PlayGameDetail.as_view(), name="play-game"),
    path("users/<str:username>/", user.UserDetail.as_view(), name="user-details"),
]
