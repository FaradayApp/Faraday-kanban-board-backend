from rest_framework import status, exceptions
from rest_framework.views import exception_handler
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


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
            response.status_code = status.HTTP_401_UNAUTHORIZED
        elif isinstance(exc, exceptions.PermissionDenied):
            response.status_code = status.HTTP_403_FORBIDDEN
        elif isinstance(exc, exceptions.ValidationError):
            errors = {}
            for key, value in response.data.items():
                if type(value) is list:
                    k, v = _handle_list_item(prefix=key, items=value)
                    errors[k] = v
                elif type(value) is dict:
                    k, v = __handle_dict_item(prefix=key, item=value)
                    errors[k] = v
                elif isinstance(value, str):
                    errors[key] = str(value)

            response.data = {
                'detail': 'Validation error',
                'errors': errors
            }
    return response


def _handle_list_item(prefix: str, items: list) -> tuple:
    for item in items:
        if type(item) is dict and item:
            return __handle_dict_item(prefix, item)
        elif type(item) is list and item:
            return _handle_list_item(prefix, item)
        elif item:
            return (prefix, item)


def __handle_dict_item(prefix: str, item: dict) -> tuple:
    for k, v in item.items():
        if type(v) is dict and v:
            return __handle_dict_item(f"{prefix}_{k}", v)
        elif type(v) is list and v:
            return _handle_list_item(f"{prefix}_{k}", v)

