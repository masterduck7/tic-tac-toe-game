from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.lib.constants import GameConstants
from game.lib import exceptions as game_exceptions
from game.models import Game, User
from game.serializers import game as game_serializers


class GamesList(APIView):
    """
    List all games and optional filter by available games
    """

    def get(self, request, format=None):
        if request.GET.get("status") == "waiting":
            games = Game.objects.filter(status=GameConstants.STATUS_WAITING)
            serializer = game_serializers.AvailableGameSerializer(games, many=True)
        else:
            games = Game.objects.all()
            serializer = game_serializers.GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = game_serializers.GameInputSerializer(data=request.data)
        if serializer.is_valid():
            game = Game.objects.create(
                name=serializer.data["name"],
            )
            user, _ = User.objects.get_or_create(
                username=serializer.data["username"],
            )
            game.users.add(user)
            game.save()

            serializer = game_serializers.GameCreatedSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise game_exceptions.SerializerException


class GameDetail(APIView):
    """
    Retrieve a game instance and update users
    """

    def get_object(self, name):
        try:
            return Game.objects.get(name=name)
        except Game.DoesNotExist:
            raise game_exceptions.GameNotFoundException

    def get(self, request, name, format=None):
        game = self.get_object(name)
        serializer = game_serializers.GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, name, format=None):
        serializer = game_serializers.GameInputSerializer(data=request.data)
        if serializer.is_valid():
            game = self.get_object(name)
            if game.users.count() >= 2:
                raise game_exceptions.FullGameStatusException

            user = User.objects.get(username=serializer.data["username"])
            game.users.add(user)

            if game.users.all().count() == 2:
                game.status = GameConstants.STATUS_IN_GAME
                game.actual_player = game.users.all().first()
                game.save()

                serializer = game_serializers.InitGameSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise game_exceptions.SerializerException


class PlayGameDetail(APIView):
    """
    Play the game
    """

    def get_object(self, name):
        try:
            return Game.objects.get(name=name)
        except Game.DoesNotExist:
            raise game_exceptions.GameNotFoundException

    def get(self, request, name, format=None):
        game = self.get_object(name)
        serializer = game_serializers.GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, name, format=None):
        serializer = game_serializers.UserPlayGameInputSerializer(data=request.data)
        if serializer.is_valid():
            game = self.get_object(name)
            game.check_status
            game.check_actual_player(serializer.data["username"])
            game.check_movement(
                movement_x=serializer.data["movement_x"],
                movement_y=serializer.data["movement_y"],
            )
            winner = game.check_winner
            if winner:
                serializer = game_serializers.GameFinishedSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = game_serializers.GameSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise game_exceptions.SerializerException
