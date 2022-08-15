import json
import logging
from typing import Dict

from django.db import IntegrityError, transaction
from pydantic import ValidationError

from application.apps.dealer.exceptions import (DealerAlreadyExists,
                                                EmailAlreadyExists,
                                                InvalidDealerData)
from application.apps.dealer.models import Dealer
from application.apps.dealer.schemas import DealerData
from application.apps.user.exceptions import CPFAlreadyInUse
from application.apps.user.models import User

logger = logging.getLogger(__name__)


def create_dealer(data: Dict) -> Dealer:
    try:
        user_data: DealerData = DealerData(**data)

        with transaction.atomic():
            user = User.objects.create_user(user_data.cpf, user_data.password)
            dealer = Dealer.objects.create(
                name=user_data.name,
                email=user_data.email,
                user=user
            )

        logger.info('Succefully created dealer: %s', data)

        return dealer

    except ValidationError as e:
        error_details = json.loads(e.json())
        logger.error(f'Error when validating dealer data: {error_details}')

        raise InvalidDealerData(detail=error_details)

    except CPFAlreadyInUse:
        logger.error('There is another user using this document: %s', {'cpf': user_data.cpf})

        raise DealerAlreadyExists()

    except IntegrityError:
        logger.error('There is another user using this email: %s', {'email': user_data.email})

        raise EmailAlreadyExists()
