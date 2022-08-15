from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from application.apps.api.v1.serializers.error import \
    GenericErrorResponseSerializer
from application.apps.api.v1.serializers.order import (
    AccumulatedCashbackResponseSerializer, CreateOrderRequestSerializer,
    OrderListSerializer)
from application.apps.order.exceptions import (DealerNotExists,
                                               ExternalServiceBroken,
                                               InvalidOrderData,
                                               OrderAlreadyExists)
from application.apps.order.services import (create_order,
                                             get_accumulated_cashback,
                                             list_orders)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=CreateOrderRequestSerializer,
        responses={
            201: openapi.Response(description="Creates dealer order", schema=None),
            400: openapi.Response(
                description="Invalid order data",
                schema=GenericErrorResponseSerializer
            ),
            404: openapi.Response(
                description="Dealer not exists",
                schema=GenericErrorResponseSerializer
            ),
            409: openapi.Response(
                description="Order already exists",
                schema=GenericErrorResponseSerializer
            )
        }
    )
    def post(self, request) -> Response:
        try:
            create_order(request.data)

        except DealerNotExists as e:
            return Response({'detail': e.detail}, status=status.HTTP_404_NOT_FOUND)

        except OrderAlreadyExists as e:
            return Response({'detail': e.detail}, status=status.HTTP_409_CONFLICT)

        except InvalidOrderData as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List dealer orders", schema=OrderListSerializer
            )
        }
    )
    def get(self, request) -> Response:
        orders = list_orders(request.user)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(orders, request)
        serializer = OrderListSerializer(result_page, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class AccumulatedCashbackView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Get Accumulated cashback",
                schema=AccumulatedCashbackResponseSerializer
            ),
            500: openapi.Response(
                description="External service unavailable",
                schema=GenericErrorResponseSerializer
            )
        }
    )
    def get(self, request) -> Response:
        cpf = request.user.cpf

        try:
            accumulated_cashback = get_accumulated_cashback(cpf)

        except ExternalServiceBroken:
            return Response(
                {'detail': 'Server is unstable, please try once again later'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(accumulated_cashback, status=status.HTTP_200_OK)
