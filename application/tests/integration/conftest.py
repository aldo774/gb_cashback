import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from application.apps.dealer.services import create_dealer


@pytest.fixture
def dealer():
    return create_dealer({
        'name': 'John Wick',
        'email': 'mail@mail.com',
        'cpf': '568.211.070-68',
        'password': 'password'
    })


@pytest.fixture
def unauthorized_client():
    client = APIClient()
    return client


@pytest.fixture
def client(dealer):
    client = APIClient()
    refresh = RefreshToken.for_user(dealer.user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
