# pylint: disable=import-error
import jwt

from models import User


class NotFoundError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class AuthenticationRepository:
    def __init__(self, session, secret):
        self._session = session
        self._secret = secret

    def get_user(self, username):
        user = self._session.query(User).get(username)
        if not user:
            raise NotFoundError()

        return user

    def get_token(self, user):
        return jwt.encode({"user": user.username}, self._secret, algorithm="HS256")

    def verify_token(self, token):
        try:
            jwt.decode(token, self._secret, algorithms="HS256")
            return True
        except Exception as error:
            raise InvalidTokenError() from error
