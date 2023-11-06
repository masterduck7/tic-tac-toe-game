from django.urls import path

from game.views import user

app_name = "game"

urlpatterns = [
    path("users/<str:username>/", user.UserDetail.as_view()),
]
