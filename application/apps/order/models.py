from django.db import models

from application.apps.base.models import StandardModelMixin
from application.apps.dealer.models import Dealer


class Order(StandardModelMixin):
    """"
    Dealers Orders
    """

    class Status(models.TextChoices):
        TO_VALIDATE = 'to_validate', 'Aguardando Validação'
        APPROVED = 'approved', 'Aprovado'
        REJECTED = 'rejected', 'Rejeitado'

    dealer = models.ForeignKey(Dealer, on_delete=models.DO_NOTHING, related_name='orders')

    code = models.CharField(max_length=20, unique=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=13, choices=Status.choices, default=Status.TO_VALIDATE)


class Cashback(StandardModelMixin):
    """"
    Cashback from order
    """

    class Status(models.TextChoices):
        TO_VALIDATE = 'to_validate', 'Aguardando Validação'
        APPROVED = 'approved', 'Aprovado'
        REJECTED = 'rejected', 'Rejeitado'

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='cashback')

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    percentage = models.DecimalField(max_digits=5, decimal_places=2)


class CashbackRule(StandardModelMixin):
    """"
    Rule to calculate cashback percentage over order.
    """

    smallest_value = models.DecimalField(max_digits=10, decimal_places=2)

    biggest_value = models.DecimalField(max_digits=10, decimal_places=2)

    coefficient = models.DecimalField(max_digits=5, decimal_places=2)
