from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.lib.constants import GameConstants
from game.lib import exceptions as game_exceptions
from game.lib import swagger as game_swagger
from game.models import Game, User, UserGame
from game.serializers import game as game_serializers


class GamesList(APIView):
    @swagger_auto_schema(
        responses=game_swagger.GameList.get_response_schemas,
        manual_parameters=[game_swagger.GameList.get_query_param],
    )
    def get(self, request, format=None):
        """
        List all games and optional filter by available games
        """
        if request.GET.get("status") == "waiting":
            games = Game.objects.filter(status=GameConstants.STATUS_WAITING)
            serializer = game_serializers.AvailableGameSerializer(games, many=True)
        else:
            games = Game.objects.all()
            serializer = game_serializers.GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=game_swagger.GameList.post_response_schemas,
        request_body=game_swagger.GameList.post_request_schemas,
    )
    def post(self, request, format=None):
        """
        Create a game. User is created also, if the user sent it does not exist.
        """
        serializer = game_serializers.GameInputSerializer(data=request.data)
        if serializer.is_valid():
            game = Game.objects.create(
                name=serializer.data["name"],
            )
            user, _ = User.objects.get_or_create(
                username=serializer.data["username"],
            )
            game.players.add(user)
            game.save()

            user_game = UserGame.objects.get(user=user, game=game)
            user_game.mark = GameConstants.MARK_X
            user_game.save()

            serializer = game_serializers.GameCreatedSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise game_exceptions.SerializerException


class GameDetail(APIView):
    def get_object(self, name):
        try:
            return Game.objects.get(name=name)
        except Game.DoesNotExist:
            raise game_exceptions.GameNotFoundException

    @swagger_auto_schema(
        responses=game_swagger.GameDetail.get_response_schemas,
    )
    def get(self, request, name, format=None):
        """
        Retrieve a game instance
        """
        game = self.get_object(name)
        serializer = game_serializers.GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=game_swagger.GameDetail.put_response_schemas,
        request_body=game_swagger.GameDetail.put_request_schemas,
    )
    def put(self, request, name, format=None):
        """
        Add a new user to the game. If the game is filled it starts.
        """
        serializer = game_serializers.GameUpdateInputSerializer(data=request.data)
        if serializer.is_valid():
            game = self.get_object(name)
            if game.players.count() >= 2:
                raise game_exceptions.FullGameStatusException

            user, _ = User.objects.get_or_create(
                username=serializer.data["username"],
            )
            game.players.add(user)

            if game.players.all().count() == 2:
                user_game = UserGame.objects.get(user=user, game=game)
                user_game.mark = GameConstants.MARK_O
                user_game.save()

                game.status = GameConstants.STATUS_IN_GAME
                game.actual_player = game.players.all().first()
                game.save()

                serializer = game_serializers.InitGameSerializer(game)

                if game.status == GameConstants.STATUS_IN_GAME:
                    actual_mark = {
                        "actual_mark": UserGame.objects.get(
                            user=game.actual_player, game=game
                        ).mark
                    }
                else:
                    actual_mark = {}

                response = {**serializer.data, **actual_mark}
                return Response(response, status=status.HTTP_200_OK)
        else:
            raise game_exceptions.SerializerException


class PlayGameDetail(APIView):
    def get_object(self, name):
        try:
            return Game.objects.get(name=name)
        except Game.DoesNotExist:
            raise game_exceptions.GameNotFoundException

    @swagger_auto_schema(
        responses=game_swagger.PlayGameDetail.get_response_schemas,
    )
    def get(self, request, name, format=None):
        """
        Get the actual game details.
        """
        game = self.get_object(name)
        serializer = game_serializers.GameSerializer(game)

        if game.status == GameConstants.STATUS_IN_GAME:
            actual_mark = {
                "actual_mark": UserGame.objects.get(
                    user=game.actual_player, game=game
                ).mark
            }
        else:
            actual_mark = {}

        response = {**serializer.data, **actual_mark}
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=game_swagger.PlayGameDetail.post_response_schemas,
        request_body=game_swagger.PlayGameDetail.post_request_schemas,
    )
    def post(self, request, name, format=None):
        """
        Play the game making a movement.
        """
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

                if game.status == GameConstants.STATUS_IN_GAME:
                    actual_mark = {
                        "actual_mark": UserGame.objects.get(
                            user=game.actual_player, game=game
                        ).mark
                    }
                else:
                    actual_mark = {}

                response = {**serializer.data, **actual_mark}
                return Response(response, status=status.HTTP_200_OK)
        else:
            raise game_exceptions.SerializerException
