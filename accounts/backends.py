from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import CustomUser


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None

        except ObjectDoesNotExist:
            return None


    def get_user(self, user_id: int):
        try:
            user = CustomUser.objects.get(pk=user_id)
            return user
        except ObjectDoesNotExist:
            return None