from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from application.apps.base.models import StandardModelMixin
from application.apps.user.managers import UserManager


class User(AbstractBaseUser, StandardModelMixin):
    cpf = models.CharField(max_length=20, verbose_name='CPF', unique=True)

    password = models.CharField(max_length=255, verbose_name='Password')

    objects = UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['password']
