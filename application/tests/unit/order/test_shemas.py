from datetime import datetime

import pytest
from pydantic import ValidationError

from application.apps.order.schemas import OrderData


@pytest.fixture
def mocked_is_cpf_valid(mocker):
    return mocker.patch('application.apps.order.schemas.is_cpf_valid')


def test_should_intance_dealer_data(mocked_is_cpf_valid):
    mocked_is_cpf_valid.return_value = True

    OrderData(
        code='Acode',
        cpf='232.909.260-10',
        amount=10.5,
        date=datetime.now()
    )
    mocked_is_cpf_valid.assert_called_once()


def test_shouldnt_intance_dealer_data_due_invalid_cpf(mocked_is_cpf_valid):
    mocked_is_cpf_valid.return_value = False

    with pytest.raises(ValidationError):
        OrderData(
            code='Acode',
            cpf='232.909.260-10',
            amount=10.5,
            date=datetime.now()
        )

    mocked_is_cpf_valid.assert_called_once()
