from rest_framework import serializers


class GenericErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
