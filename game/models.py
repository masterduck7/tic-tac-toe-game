import json
from typing import Optional
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

    @property
    def check_status(self) -> Optional[bool]:
        if self.status != GameConstants.STATUS_IN_GAME:
            raise Exception

    def check_actual_player(self, username: str) -> Optional[bool]:
        if self.actual_player.username != username:
            raise Exception

    def check_movement(self, movement_x: int, movement_y: int) -> Optional[bool]:
        decoded_board = json.loads(self.board)
        if decoded_board[movement_x][movement_y] == 0:
            decoded_board[movement_x][movement_y] = self.actual_player.username
            self.board = json.dumps(decoded_board)
            self.actual_player = self.users.exclude(
                username=self.actual_player.username
            ).first()
            self.save()
        else:
            raise Exception

    @property
    def check_winner(self) -> Optional[bool]:
        decoded_board = json.loads(self.board)

        # Check horizontal
        for row in range(len(decoded_board)):
            winner = True
            for col in range(len(decoded_board)):
                if decoded_board[row][col] != self.actual_player.username:
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
                if decoded_board[col][row] != self.actual_player.username:
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
            if decoded_board[row][row] != self.actual_player.username:
                winner = False
                break
        if winner:
            self.status = GameConstants.STATUS_FINISHED
            self.winner = self.actual_player
            self.save()
            return True

        winner = True
        for row in range(len(decoded_board)):
            if (
                decoded_board[row][len(decoded_board) - 1 - row]
                != self.actual_player.username
            ):
                winner = False
                break
        if winner:
            self.status = GameConstants.STATUS_FINISHED
            self.winner = self.actual_player
            self.save()
            return True
