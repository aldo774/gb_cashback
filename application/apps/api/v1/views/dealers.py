from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from application.apps.api.v1.serializers.dealer import \
    CreateDealerRequestSerializer
from application.apps.api.v1.serializers.error import \
    GenericErrorResponseSerializer
from application.apps.dealer.exceptions import (DealerAlreadyExists,
                                                EmailAlreadyExists,
                                                InvalidDealerData)
from application.apps.dealer.services import create_dealer


class DealerView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=CreateDealerRequestSerializer,
        responses={
            201: openapi.Response(description="Creates dealer", schema=None),
            400: openapi.Response(
                description="Invalid dealer data",
                schema=GenericErrorResponseSerializer
            ),
            409: openapi.Response(
                description="Dealer already exists(cpf or email)",
                schema=GenericErrorResponseSerializer
            )
        }
    )
    def post(self, request) -> Response:
        try:
            create_dealer(request.data)

        except (DealerAlreadyExists, EmailAlreadyExists) as e:
            return Response({'detail': e.detail}, status=status.HTTP_409_CONFLICT)

        except InvalidDealerData as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
