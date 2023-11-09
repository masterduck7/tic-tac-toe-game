from drf_yasg import openapi

from game.lib import exceptions as game_exceptions
from game.lib.constants import GameConstants


class UserList:
    response_schemas = {
        "201": openapi.Response(
            description="User created",
            examples={
                "application/json": {
                    "username": "Tom",
                    "number_of_games": "1",
                    "points": "1",
                }
            },
        ),
        "400": openapi.Response(
            description="Serializer error",
            examples={
                "application/json": {
                    "detail": game_exceptions.SerializerException.default_detail
                }
            },
        ),
    }

    request_schemas = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
        },
    )


class UserDetail:
    response_schemas = {
        "200": openapi.Response(
            description="User details",
            examples={
                "application/json": {
                    "user": {
                        "username": "Tom",
                        "number_of_games": "1",
                        "points": "1",
                    },
                    "games": [
                        {
                            "name": "Lets play",
                            "status": GameConstants.STATUS_FINISHED,
                            "players": [
                                {"username": "Tom"},
                                {"username": "Jerry"},
                            ],
                            "actual_player": None,
                            "board": "[[Tom,Tom,Tom],[Jerry,Jerry,0],[0,0,0]]",
                            "winner": {
                                "username": "Tom",
                            },
                        }
                    ],
                }
            },
        ),
        "404": openapi.Response(
            description="User not found",
            examples={"application/json": {"detail": "User Not Found."}},
        ),
    }


class GameList:
    get_response_schemas = {
        "200": openapi.Response(
            description="Games list",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_IN_GAME,
                        "players": [
                            {"username": "Tom"},
                            {"username": "Jerry"},
                        ],
                        "actual_player": {
                            "username": "Tom",
                        },
                        "board": "[[Tom,Tom,0],[Jerry,Jerry,0],[0,0,0]]",
                        "winner": {
                            "username": "Tom",
                        },
                    }
                ]
            },
        ),
        "200 ": openapi.Response(
            description="Available Games",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_WAITING,
                    },
                    {
                        "name": "A new game",
                        "status": GameConstants.STATUS_WAITING,
                    },
                ]
            },
        ),
    }

    get_query_param = openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        description="Filter by availables sending waiting here",
        type=openapi.TYPE_STRING,
    )

    post_request_schemas = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
        },
    )

    post_response_schemas = {
        "201": openapi.Response(
            description="Game Created",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_WAITING,
                        "players": [
                            {"username": "Tom"},
                        ],
                    }
                ]
            },
        ),
        "400": openapi.Response(
            description="Serializer error",
            examples={
                "application/json": {
                    "detail": game_exceptions.SerializerException.default_detail
                }
            },
        ),
    }


class GameDetail:
    get_response_schemas = {
        "200": openapi.Response(
            description="Game details",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_IN_GAME,
                        "players": [
                            {"username": "Tom"},
                            {"username": "Jerry"},
                        ],
                        "actual_player": {
                            "username": "Tom",
                        },
                        "board": "[[Tom,Tom,0],[Jerry,Jerry,0],[0,0,0]]",
                        "winner": {
                            "username": "Tom",
                        },
                    }
                ]
            },
        ),
        "404": openapi.Response(
            description="Game not found",
            examples={"application/json": {"detail": "Game Not Found."}},
        ),
    }

    post_request_schemas = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
        },
    )

    post_response_schemas = {
        "200": openapi.Response(
            description="Game updated",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_IN_GAME,
                        "players": [
                            {"username": "Tom"},
                            {"username": "Jerry"},
                        ],
                        "actual_player": {
                            "username": "Tom",
                        },
                    }
                ]
            },
        ),
        "400": openapi.Response(
            description="Serializer error",
            examples={
                "application/json": {
                    "detail": game_exceptions.SerializerException.default_detail
                }
            },
        ),
        "400 ": openapi.Response(
            description="Full game error. The game have the maximum number of users and is in game.",
            examples={
                "application/json": {
                    "detail": game_exceptions.FullGameStatusException.default_detail
                }
            },
        ),
    }


class PlayGameDetail:
    get_response_schemas = {
        "200": openapi.Response(
            description="Game details",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_IN_GAME,
                        "players": [
                            {"username": "Tom"},
                            {"username": "Jerry"},
                        ],
                        "actual_player": {
                            "username": "Tom",
                        },
                        "board": "[[Tom,Tom,0],[Jerry,Jerry,0],[0,0,0]]",
                        "winner": {
                            "username": "Tom",
                        },
                    }
                ]
            },
        ),
        "404": openapi.Response(
            description="Game not found",
            examples={"application/json": {"detail": "Game Not Found."}},
        ),
    }

    post_request_schemas = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
            "movement_x": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
            "movement_y": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
        },
    )

    post_response_schemas = {
        "200": openapi.Response(
            description="Game details",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_IN_GAME,
                        "players": [
                            {"username": "Tom"},
                            {"username": "Jerry"},
                        ],
                        "actual_player": {
                            "username": "Tom",
                        },
                        "board": "[[Tom,Tom,0],[Jerry,Jerry,0],[0,0,0]]",
                        "winner": {
                            "username": "Tom",
                        },
                    }
                ]
            },
        ),
        "200 ": openapi.Response(
            description="Game finished",
            examples={
                "application/json": [
                    {
                        "name": "Lets play",
                        "status": GameConstants.STATUS_FINISHED,
                        "winner": {
                            "username": "Tom",
                        },
                    }
                ]
            },
        ),
        "400": openapi.Response(
            description="Serializer error",
            examples={
                "application/json": {
                    "detail": game_exceptions.SerializerException.default_detail
                }
            },
        ),
    }
