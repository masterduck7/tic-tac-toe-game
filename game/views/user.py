from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.lib.exceptions import UserNotFoundException
from game.models import Game, User
from game.serializers.game import GameSerializer
from game.serializers.user import UserInputSerializer, UserSerializer


class UserDetail(APIView):
    """
    Login or register User
    """

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise UserNotFoundException

    def get(self, request, username, format=None):
        user = self.get_object(username)
        games = Game.objects.filter(users__id=user.id)
        serializer_user = UserSerializer(user)
        serializer_games = GameSerializer(games, many=True)
        data = {
            "user": serializer_user.data,
            "games": serializer_games.data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserInputSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.data["username"],
            )
            serializer = UserSerializer(user)

            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
