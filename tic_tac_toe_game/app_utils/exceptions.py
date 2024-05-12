class PositionNotEmptyException(Exception):
    """
    Custom exception class to handle if the position is not empty exception.
    """

    def __init__(self) -> None:
        self.message = "Position is not empty."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}"


class BoardFullException(Exception):
    """
    Custom exception class to handle if the the Board is full.
    """

    def __init__(self) -> None:
        self.message = "Board is full. Game Complete...."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}"


class GameCompleteException(Exception):
    """
    Custom exception class to handle if the any player has completed the game.
    """

    def __init__(self) -> None:
        self.message = "consecutive match. Game Complete..."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}"
