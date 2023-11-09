import json
from typing import Optional
from django.db import models

from game.lib.constants import GameConstants
from game.lib import exceptions as game_exceptions


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
        default='[["","",""],["","",""],["","",""]]',
        blank=None,
    )
    players = models.ManyToManyField(
        User,
        related_name="users",
        related_query_name="game",
        through="UserGame",
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

    @property
    def check_status(self) -> Optional[bool]:
        if self.status != GameConstants.STATUS_IN_GAME:
            raise game_exceptions.NotValidGameStatusException

    def check_actual_player(self, username: str) -> Optional[bool]:
        if self.actual_player.username != username:
            raise game_exceptions.NotUserTurnException

    def check_movement(self, movement_x: int, movement_y: int) -> Optional[bool]:
        decoded_board = json.loads(self.board)
        if (
            movement_x in GameConstants.VALID_POSITIONS
            and movement_y in GameConstants.VALID_POSITIONS
            and decoded_board[movement_x][movement_y] == ""
        ):
            character = UserGame.objects.get(
                user=self.actual_player, game=self
            ).character
            decoded_board[movement_x][movement_y] = character
            self.board = json.dumps(decoded_board)
            self.save()
        else:
            raise game_exceptions.NotValidPositionException

    @property
    def change_player(self):
        self.actual_player = self.players.exclude(
            username=self.actual_player.username
        ).first()
        self.save()

    @property
    def check_winner(self) -> Optional[bool]:
        decoded_board = json.loads(self.board)
        actual_character = UserGame.objects.get(
            user=self.actual_player, game=self
        ).character

        # Check horizontal
        for row in range(len(decoded_board)):
            winner = True
            for col in range(len(decoded_board)):
                if decoded_board[row][col] != actual_character:
                    winner = False
                    break
            if winner:
                self.status = GameConstants.STATUS_FINISHED
                self.winner = self.actual_player
                self.save()
                return True

        # Check vertical
        for row in range(len(decoded_board)):
            winner = True
            for col in range(len(decoded_board)):
                if decoded_board[col][row] != actual_character:
                    winner = False
                    break
            if winner:
                self.status = GameConstants.STATUS_FINISHED
                self.winner = self.actual_player
                self.save()
                return True

        # Check diagonals
        winner = True
        for row in range(len(decoded_board)):
            if decoded_board[row][row] != actual_character:
                winner = False
                break
        if winner:
            self.status = GameConstants.STATUS_FINISHED
            self.winner = self.actual_player
            self.save()
            return True

        winner = True
        for row in range(len(decoded_board)):
            if decoded_board[row][len(decoded_board) - 1 - row] != actual_character:
                winner = False
                break
        if winner:
            self.status = GameConstants.STATUS_FINISHED
            self.winner = self.actual_player
            self.winner.points += 1
            self.actual_player = None
            self.save()
            for user in self.players.all():
                user.number_of_games += 1
                user.save()
            return True
        else:
            self.change_player


class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    character = models.CharField(
        max_length=1,
        blank=False,
        null=False,
        choices=GameConstants.CHARACTERS_CHOICES,
    )

    class Meta:
        unique_together = ("user", "game")
