from django.db import models

from application.apps.base.models import StandardModelMixin
from application.apps.user.models import User


class Dealer(StandardModelMixin):
    name = models.CharField(max_length=255, verbose_name='Name')

    email = models.CharField(max_length=255, verbose_name='Email', unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.name, self.email)
