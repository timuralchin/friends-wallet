class BaseCoreException(Exception):
    """Base exceptions."""

    default_message = None

    def __init__(self, message=None):
        """Added default message for errors."""
        if message is None:
            message = self.default_message

        super().__init__(message)
