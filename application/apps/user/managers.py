from django.contrib.auth.base_user import BaseUserManager
from django.db import IntegrityError

from application.apps.user.exceptions import CPFAlreadyInUse


class UserManager(BaseUserManager):
    """
    Custom user model manager where CPF is the unique identifier for
    authentication.
    """
    def create_user(self, cpf, password, **extra_fields):
        """
        Create and save a User with CPF and password.
        """
        try:
            user = self.model(cpf=cpf, **extra_fields)
            user.set_password(password)
            user.save()

        except IntegrityError:
            raise CPFAlreadyInUse()

        return user
