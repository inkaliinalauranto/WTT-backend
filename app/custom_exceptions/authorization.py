class CredentialsException(Exception):
    def __init__(self, message: str):
        self.message = message

class UnauthorizedAccessException(Exception):
    def __init__(self, message: str):
        self.message = message

class UnauthorizedActionException(Exception):
    def __init__(self, message: str):
        self.message = message
