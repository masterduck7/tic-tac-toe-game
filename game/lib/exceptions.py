from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = "User Not Found."


class GameNotFoundException(APIException):
    status_code = 404
    default_detail = "Game Not Found."


class NotValidGameStatusException(APIException):
    status_code = 400
    default_detail = "Game status is not valid for this action."


class NotUserTurnException(APIException):
    status_code = 400
    default_detail = "The turn to play is for the other player. Please wait until this turn finishes."


class NotValidPositionException(APIException):
    status_code = 400
    default_detail = (
        "The position selected is not possible. Please select an empty space."
    )
