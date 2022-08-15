from rest_framework import serializers


class CreateDealerRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    cpf = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
