from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.lib import exceptions as game_exceptions
from game.lib import swagger as game_swagger
from game.models import Game, User
from game.serializers.game import GameSerializer
from game.serializers.user import UserInputSerializer, UserSerializer


class UserList(APIView):
    @swagger_auto_schema(
        responses=game_swagger.UserList.response_schemas,
        request_body=game_swagger.UserList.request_schemas,
    )
    def post(self, request, format=None):
        """
        Register a new User.
        """
        serializer = UserInputSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.data["username"],
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise game_exceptions.SerializerException


class UserDetail(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise game_exceptions.UserNotFoundException

    @swagger_auto_schema(responses=game_swagger.UserDetail.response_schemas)
    def get(self, request, username, format=None):
        """
        Login User and get user data with the games played.
        """
        user = self.get_object(username)
        games = Game.objects.filter(players__id=user.id)
        serializer_user = UserSerializer(user)
        serializer_games = GameSerializer(games, many=True)
        data = {
            "user": serializer_user.data,
            "games": serializer_games.data,
        }
        return Response(data, status=status.HTTP_200_OK)
