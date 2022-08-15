from datetime import datetime

import pytest
from django.db import IntegrityError
from pydantic import ValidationError

from application.apps.dealer.models import Dealer
from application.apps.order.exceptions import (DealerNotExists,
                                               InvalidOrderData,
                                               OrderAlreadyExists)
from application.apps.order.services import create_order


@pytest.fixture
def mocked_order_data(mocker):
    return mocker.patch('application.apps.order.services.OrderData')


@pytest.fixture
def mocked_dealer_get(mocker):
    return mocker.patch('application.apps.order.services.Dealer.objects.get')


@pytest.fixture
def mocked_create_cashback(mocker):
    return mocker.patch('application.apps.order.services.create_cashback')


@pytest.fixture
def mocked_model_order_create(mocker):
    return mocker.patch('application.apps.order.services.Order.objects.create')


@pytest.fixture
def mocked_transaction(mocker):
    return mocker.patch('application.apps.order.services.transaction')


def test_shouldnt_create_order_due_validation_error(mocker, mocked_order_data):
    error = ValidationError(mocker.MagicMock(), model=mocker.MagicMock())
    error.json = mocker.MagicMock(return_value='{}')
    mocked_order_data.side_effect = error

    with pytest.raises(InvalidOrderData):
        create_order({
            'code': 'Acode',
            'cpf': '232.909.260-10',
            'amount': 10.5,
            'date': datetime.now()
        })


@pytest.mark.usefixtures("mocked_order_data")
def test_shouldnt_create_order_due_non_existent_dealer(mocked_dealer_get):
    mocked_dealer_get.side_effect = Dealer.DoesNotExist()

    with pytest.raises(DealerNotExists):
        create_order({
            'code': 'Acode',
            'cpf': '232.909.260-10',
            'amount': 10.5,
            'date': datetime.now()
        })


@pytest.mark.usefixtures(
    "mocked_order_data",
    "mocked_dealer_get",
    "mocked_create_cashback",
    "mocked_transaction"
)
def test_shouldnt_create_order_due_integrity_error(mocked_model_order_create):
    mocked_model_order_create.side_effect = IntegrityError()

    with pytest.raises(OrderAlreadyExists):
        create_order({
            'code': 'Acode',
            'cpf': '232.909.260-10',
            'amount': 10.5,
            'date': datetime.now()
        })


@pytest.mark.usefixtures("mocked_transaction")
def test_should_create_order(
    mocked_order_data,
    mocked_dealer_get,
    mocked_create_cashback,
    mocked_model_order_create
):
    create_order({
        'code': 'Acode',
        'cpf': '232.909.260-10',
        'amount': 10.5,
        'date': datetime.now()
    })

    mocked_order_data.assert_called_once()
    mocked_dealer_get.assert_called_once()
    mocked_create_cashback.assert_called_once()
    mocked_model_order_create.assert_called_once()
