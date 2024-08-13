class APIException(Exception):
    """An exception for when something goes wrong in the API."""

    def __init__(
        self, message: str = "An exception happened in the Prompt Bouncer API!"
    ):
        self.message = message
        super().__init__(self.message)
