import pytest
import requests
from rest_framework import status

from application.apps.order.exceptions import ExternalServiceBroken
from application.apps.order.services import get_accumulated_cashback


@pytest.fixture
def mocked_request(mocker):
    return mocker.patch('application.apps.order.services.requests.get')


def test_shouldnt_get_accumulated_cashback_due_external_service_broken(mocker, mocked_request):
    response_mocked = mocker.MagicMock(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        raise_for_status=mocker.MagicMock()
    )
    response_mocked.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mocker.MagicMock()
    )

    mocked_request.return_value = response_mocked
    with pytest.raises(ExternalServiceBroken):
        get_accumulated_cashback('1234')


def test_should_get_accumulated_cashback(mocker, mocked_request):
    response_mocked = mocker.MagicMock(
        status_code=status.HTTP_200_OK, json=mocker.MagicMock()
    )
    response_mocked.json.return_value = {'body': {'credit': 4000}}
    mocked_request.return_value = response_mocked

    res = get_accumulated_cashback('1234')
    assert res == {'credit': 4000}
