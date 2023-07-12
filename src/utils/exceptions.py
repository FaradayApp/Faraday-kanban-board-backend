from rest_framework import status
from typing import Optional


class CustomException(Exception):
    _status = status.HTTP_400_BAD_REQUEST
    _message = ""

    def __init__(self, message: Optional[str] = None):
        self.message = message if message else self._message

    def get_data(self):
        return {"detail": self.message}

    @classmethod
    def get_status(cls):
        return cls._status
