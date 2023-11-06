from rest_framework import serializers


class UserInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, read_only=False)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    number_of_games = serializers.IntegerField()
    points = serializers.IntegerField()
