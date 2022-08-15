from datetime import datetime

from pydantic import BaseModel, validator

from application.apps.dealer.utils import is_cpf_valid


class OrderData(BaseModel):
    code: str
    amount: float
    date: datetime
    cpf: str

    @validator('cpf')
    def validate_cpf(cls, value):
        if not is_cpf_valid(value):
            raise ValueError('Invalid CPF')

        return value

    class Config:
        allow_mutation = False
