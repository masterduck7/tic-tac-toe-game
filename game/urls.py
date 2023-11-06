from django.urls import path

from game.views import game, user

app_name = "game"

urlpatterns = [
    path("games/", game.GamesList.as_view()),
    path("games/<str:name>/", game.GameDetail.as_view()),
    path("play/<str:name>/", game.PlayGameDetail.as_view()),
    path("users/<str:username>/", user.UserDetail.as_view()),
]
