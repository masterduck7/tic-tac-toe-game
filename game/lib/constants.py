class GameConstants:
    STATUS_WAITING = "WAITING"
    STATUS_IN_GAME = "IN_GAME"
    STATUS_FINISHED = "FINISHED"

    STATUS_CHOICES = (
        (STATUS_WAITING, "Waiting"),
        (STATUS_IN_GAME, "In Game"),
        (STATUS_FINISHED, "Finished"),
    )
