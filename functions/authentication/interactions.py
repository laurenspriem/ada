class InvalidCredentialsError(Exception):
    pass


class AuthenticationInteractions:
    def __init__(self, authentication_repository):
        self._authentication_repository = authentication_repository

    def authenticate(self, username, password):
        user = self._authentication_repository.get_user(username)

        if user.password != password:
            raise InvalidCredentialsError()

        token = self._authentication_repository.get_token(user)

        return {"token": token}

    def verify(self, token):
        return self._authentication_repository.verify_token(token)
