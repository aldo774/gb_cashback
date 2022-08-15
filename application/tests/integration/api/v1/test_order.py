import json
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from application.apps.order.models import Cashback, CashbackRule, Order


@pytest.mark.django_db
class TestOrders:
    @pytest.fixture
    def order(self, dealer):
        return Order.objects.create(
            code='XPTO001',
            dealer=dealer,
            amount='1000',
            date='2022-08-11T10:40:00.000Z',
        )

    @pytest.fixture
    def cashback(self, order):
        return Cashback.objects.create(
            order=order,
            amount=Decimal('100'),
            percentage=Decimal('.1'),
        )

    @pytest.fixture
    def cashback_rule(self):
        return CashbackRule.objects.create(
            smallest_value=1500,
            biggest_value=9999999,
            coefficient=0.15
        )

    @pytest.fixture
    def payload(self):
        return {
            'code': 'XPTO001',
            'cpf': '568.211.070-68',
            'amount': 10000,
            'date': '2022-08-11T10:40:00.000Z'
        }

    def test_should_unauthorize(self, unauthorized_client, payload):
        unauthorized_client.credentials()

        response = unauthorized_client.post(
            reverse('orders'), json.dumps(payload), content_type='application/json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_shouldnt_create_order_due_non_existent_cpf(self, client, payload):
        payload['cpf'] = '159.382.760-12'

        response = client.post(
            reverse('orders'), json.dumps(payload), content_type='application/json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Dealer does not Exists'}

    @pytest.mark.usefixtures("order")
    def test_shouldnt_create_order_due_duplicating_code(self, client, payload):
        response = client.post(
            reverse('orders'), json.dumps(payload), content_type='application/json'
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {'detail': 'Order already exists'}

    @pytest.mark.usefixtures("cashback_rule")
    def test_should_create_an_order(self, client, payload):
        response = client.post(
            reverse('orders'), json.dumps(payload), content_type='application/json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.usefixtures("cashback_rule")
    def test_should_create_an_approved_order(self, client, payload, dealer):
        dealer.verified = True
        dealer.save()
        assert not dealer.orders.count()

        response = client.post(
            reverse('orders'), json.dumps(payload), content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert dealer.orders.count() == 1
        assert dealer.orders.first().status == Order.Status.APPROVED

    @pytest.mark.usefixtures("cashback")
    def test_should_list_orders(self, client):

        response = client.get(reverse('orders'))

        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data[0]['code'] == 'XPTO001'
