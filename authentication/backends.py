from django.http import HttpRequest
from django.contrib.auth.backends import BaseBackend

from database.models import Users


class SimpleAuthBackend(BaseBackend):
    def authenticate(self, request: HttpRequest, username = None, password = None, **kwargs):  # type: ignore
        if not username or not password:
            return None

        try:
            user = (
                Users.objects.get(email=username)
                if "@" in username
                else Users.objects.get(username=username)
            )
            if user.password == password:
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id: int):  # type: ignore
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
