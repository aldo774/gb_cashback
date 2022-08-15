import json
import logging
from typing import Dict

from django.db import IntegrityError, transaction
from django.db.models.query import QuerySet
from pydantic import ValidationError

from application.apps.dealer.models import Dealer
from application.apps.order.exceptions import (DealerNotExists,
                                               InvalidOrderData,
                                               OrderAlreadyExists)
from application.apps.order.models import Order
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
