from decimal import Decimal

from rest_framework import serializers

from application.apps.order.models import Order


class AccumulatedCashbackResponseSerializer(serializers.Serializer):
    credit = serializers.DecimalField(max_digits=10, decimal_places=2)


class CreateOrderRequestSerializer(serializers.Serializer):
    code = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()
    cpf = serializers.CharField()


class OrderListSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()
    cpf = serializers.CharField(source='dealer.user.cpf')
    status = serializers.ChoiceField(Order.Status)
    cashback_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='cashback.amount'
    )
    cashback_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'code',
            'amount',
            'date',
            'cpf',
            'cashback_amount',
            'cashback_percentage',
            'status',
        )

    def get_cashback_percentage(self, obj):
        return f'{obj.cashback.percentage * Decimal("100")}%'
