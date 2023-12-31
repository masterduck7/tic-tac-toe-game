class GameConstants:
    STATUS_WAITING = "WAITING"
    STATUS_IN_GAME = "IN_GAME"
    STATUS_FINISHED = "FINISHED"

    STATUS_CHOICES = (
        (STATUS_WAITING, "Waiting"),
        (STATUS_IN_GAME, "In Game"),
        (STATUS_FINISHED, "Finished"),
    )

    VALID_POSITIONS = [0, 1, 2]

    MARK_X = "X"
    MARK_O = "O"
    MARK_CHOICES = (
        (MARK_X, "X"),
        (MARK_O, "O"),
    )
