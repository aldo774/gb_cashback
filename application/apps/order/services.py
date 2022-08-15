import json
import logging
from typing import Dict

import requests
from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.db.models.query import QuerySet
from pydantic import ValidationError

from application.apps.dealer.models import Dealer
from application.apps.order.exceptions import (DealerNotExists,
                                               ExternalServiceBroken,
                                               InvalidOrderData,
                                               OrderAlreadyExists)
from application.apps.order.models import Cashback, CashbackRule, Order
from application.apps.order.schemas import OrderData
from application.apps.user.models import User

logger = logging.getLogger(__name__)


def create_order(data: Dict) -> Order:
    try:
        data: OrderData = OrderData(**data)
        dealer: Dealer = Dealer.objects.get(user__cpf=data.cpf)

        values = {
            'dealer': dealer,
            'code': data.code,
            'amount': data.amount,
            'date': data.date
        }

        if dealer.verified:
            values['status'] = Order.Status.APPROVED

        with transaction.atomic():
            order = Order.objects.create(**values)
            create_cashback(order)

        logger.info('Succefully created order: %s', {'order': order.id, 'dealer': order.dealer.id})

        return order

    except ValidationError as e:
        error_details = json.loads(e.json())
        logger.error(f'Error when validating order data: {error_details}')

        raise InvalidOrderData(detail=error_details)

    except Dealer.DoesNotExist:
        logger.error('Dealer with this data does not exists: %s', {'cpf': data.cpf})
        raise DealerNotExists()

    except IntegrityError:
        logger.error(f'Order {data.code} already exists')
        raise OrderAlreadyExists()


def list_orders(user: User) -> QuerySet:
    return Order.objects.filter(dealer__user=user)


def _get_cashback_rule(value: float) -> CashbackRule:
    return CashbackRule.objects.get(
        smallest_value__lt=value,
        biggest_value__gte=value
    )


def create_cashback(order: Order) -> Cashback:
    order_amount_in_month = Order.objects.filter(
        date__year=order.date.year,
        date__month=order.date.month,
        dealer=order.dealer
    ).aggregate(Sum('amount'))['amount__sum']

    cashback_rule = _get_cashback_rule(order_amount_in_month)
    cashback = Cashback.objects.create(
        order=order,
        amount=(order.amount * float(cashback_rule.coefficient)),
        percentage=cashback_rule.coefficient
    )

    logger.info(
        'Succefully created cashback: %s', {'cashback': cashback.id, 'dealer': order.dealer.id}
    )

def get_accumulated_cashback(cpf: str):
    """
    Returns the accumulated cashback value from external service.
    """
    headers = {'token': settings.CASHBACK_EXTERNAL_SERVICE_TOKEN}

    try:
        response = requests.get(
            settings.CASHBACK_EXTERNAL_SERVICE_HOST,
            params={'cpf': cpf},
            headers=headers
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        logger.error(
            f'Error when trying to comunicate with external service: {e.response.json()}'
        )
        raise ExternalServiceBroken()

    response_data: Dict = response.json()

    return response_data['body']
