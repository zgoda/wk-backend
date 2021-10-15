class AuthError(Exception):
    def __init__(self, error: dict, status_code: int):
        self.error = error
        self.status_code = status_code
