from django.db import models

from game.lib.constants import GameConstants


class User(models.Model):
    username = models.CharField(unique=True, blank=False, max_length=100)
    number_of_games = models.IntegerField(default=0, blank=False)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Game(models.Model):
    name = models.CharField(
        default="New Game", unique=False, blank=False, max_length=100
    )
    status = models.CharField(
        choices=GameConstants.STATUS_CHOICES,
        default=GameConstants.STATUS_WAITING,
        max_length=20,
    )
    board = models.TextField(
        default="[[0,0,0],[0,0,0],[0,0,0]]",
        blank=None,
    )
    users = models.ManyToManyField(
        User,
        related_name="users",
        related_query_name="game",
        blank=False,
    )
    actual_player = models.ForeignKey(
        User,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="actual_player",
    )
    winner = models.ForeignKey(
        User,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="winner",
    )

    def __str__(self):
        return self.name
