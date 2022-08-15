import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestApiV1Dealers:

    @pytest.fixture
    def payload(self):
        return {
            'name': 'A name with last name',
            'cpf': '678.483.010-52',
            'email': 'amail@mail.com',
            'password': 'apassword'
        }

    def test_should_create_dealer(self, unauthorized_client, payload):
        unauthorized_client.credentials()
        response = unauthorized_client.post(
            reverse('dealers'),
            json.dumps(payload), content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_shouldnt_create_dealer_due_duplicated_email(
        self, unauthorized_client, payload, dealer
    ):
        payload['email'] = dealer.email
        response = unauthorized_client.post(
            reverse('dealers'),
            json.dumps(payload), content_type='application/json'
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {'detail': 'Email already exists'}

    def test_shouldnt_create_dealer_due_existing_cpf(
        self, unauthorized_client, payload, dealer
    ):
        payload['cpf'] = dealer.user.cpf
        response = unauthorized_client.post(
            reverse('dealers'),
            json.dumps(payload), content_type='application/json'
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {'detail': 'Dealer already exists'}

    def test_shouldnt_create_dealer_due_invalid_data(
        self, unauthorized_client, payload, dealer
    ):
        payload.pop('email')
        response = unauthorized_client.post(
            reverse('dealers'),
            json.dumps(payload), content_type='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'detail': [
                {'loc': ['email'], 'msg': 'field required', 'type': 'value_error.missing'}
            ]
        }
