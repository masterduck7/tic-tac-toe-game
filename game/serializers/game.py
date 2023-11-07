from rest_framework import serializers

from game.serializers.user import UserInputSerializer


class GameInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)


class AvailableGameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=100, read_only=True)


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=100, read_only=True)
    board = serializers.CharField(max_length=256, read_only=True)
    users = UserInputSerializer(many=True, read_only=True)
    actual_player = UserInputSerializer(read_only=True)
    winner = UserInputSerializer(read_only=True)


class GameCreatedSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=100, read_only=True)
    users = UserInputSerializer(many=True, read_only=True)


class InitGameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=100, read_only=True)
    users = UserInputSerializer(many=True, read_only=True)
    actual_player = UserInputSerializer(read_only=True)


class PlayGameInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    username = serializers.CharField(max_length=100)
    movement_x = serializers.IntegerField()
    movement_y = serializers.IntegerField()


class GameFinishedSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    winner = UserInputSerializer(read_only=True)
