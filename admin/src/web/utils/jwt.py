"""JWT utilities."""
import time

import jwt
from flask import Flask

DURATION = 60  # in minutes


class JWT:
    """A class for encoding and decoding JWTs."""

    def __init__(self, secret_key="", duration=DURATION * 60):
        self.secret_key = secret_key
        self.duration = duration

    def init_app(self, app: Flask):
        self.secret_key = app.config["SECRET_KEY"]
        self.duration = app.config["JWT_DURATION"]

    def encode(self, payload):
        """Encodes a JWT token"""
        payload.update({"exp": time.time() + self.duration})
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def decode(self, token) -> dict or None:
        """Decodes a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.PyJWTError:
            return None

    # ? Funcion para obtener el usuario


jwt_auth = JWT()
