import pytest
from pydantic import ValidationError

from application.apps.dealer.schemas import DealerData


@pytest.fixture
def mocked_is_cpf_valid(mocker):
    return mocker.patch('application.apps.dealer.schemas.is_cpf_valid')


def test_should_intance_dealer_data(mocked_is_cpf_valid):
    mocked_is_cpf_valid.return_value = True

    DealerData(
        name='Aname',
        cpf='232.909.260-10',
        email='amail@mail.com',
        password='apassword'
    )
    mocked_is_cpf_valid.assert_called_once()


def test_shouldnt_intance_dealer_data_due_invalid_cpf(mocked_is_cpf_valid):
    mocked_is_cpf_valid.return_value = False

    with pytest.raises(ValidationError):
        DealerData(
            name='Aname',
            cpf='232.909.260-10',
            email='amail@mail.com',
            password='apassword'
        )

    mocked_is_cpf_valid.assert_called_once()
