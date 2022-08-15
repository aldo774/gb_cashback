import pytest
from django.db import IntegrityError
from pydantic import ValidationError

from application.apps.dealer.exceptions import (DealerAlreadyExists,
                                                EmailAlreadyExists,
                                                InvalidDealerData)
from application.apps.dealer.services import create_dealer
from application.apps.user.exceptions import CPFAlreadyInUse


@pytest.fixture
def mocked_dealer_data(mocker):
    return mocker.patch('application.apps.dealer.services.DealerData')


@pytest.fixture
def mocked_create_user(mocker):
    return mocker.patch('application.apps.dealer.services.User.objects.create_user')


@pytest.fixture
def mocked_dealer_create(mocker):
    return mocker.patch('application.apps.dealer.services.Dealer.objects.create')


@pytest.fixture
def mocked_transaction(mocker):
    return mocker.patch('application.apps.dealer.services.transaction')


def test_shouldnt_create_dealer_due_validation_error(mocker, mocked_dealer_data):
    error = ValidationError(mocker.MagicMock(), model=mocker.MagicMock())
    error.json = mocker.MagicMock(return_value='{}')
    mocked_dealer_data.side_effect = error

    with pytest.raises(InvalidDealerData):
        create_dealer({
            'name': 'Aname with Last Name',
            'cpf': '232.909.260-10',
            'email': 'amail@mail.com',
            'password': 'apassword'
        })


@pytest.mark.usefixtures("mocked_dealer_data", "mocked_dealer_create", "mocked_transaction")
def test_shouldnt_create_dealer_due_cpf_already_in_use(mocked_create_user):
    mocked_create_user.side_effect = CPFAlreadyInUse()

    with pytest.raises(DealerAlreadyExists):
        create_dealer({
            'name': 'Aname with Last Name',
            'cpf': '232.909.260-10',
            'email': 'amail@mail.com',
            'password': 'apassword'
        })


@pytest.mark.usefixtures("mocked_create_user", "mocked_dealer_data", "mocked_transaction")
def test_shouldnt_create_dealer_due_integrity_error(mocked_dealer_create):
    mocked_dealer_create.side_effect = IntegrityError()

    with pytest.raises(EmailAlreadyExists):
        create_dealer({
            'name': 'Aname with Last Name',
            'cpf': '232.909.260-10',
            'email': 'amail@mail.com',
            'password': 'apassword'
        })


@pytest.mark.usefixtures("mocked_transaction")
def test_create_dealer(
    mocked_create_user, mocked_dealer_data, mocked_dealer_create
):
    create_dealer({
        'name': 'Aname with Last Name',
        'cpf': '232.909.260-10',
        'email': 'amail@mail.com',
        'password': 'apassword'
    })

    mocked_create_user.assert_called_once()
    mocked_dealer_data.assert_called_once()
    mocked_dealer_create.assert_called_once()
