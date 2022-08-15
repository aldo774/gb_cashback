from pydantic import BaseModel, EmailStr, validator

from application.apps.dealer.utils import is_cpf_valid


class DealerData(BaseModel):
    name: str
    cpf: str
    email: EmailStr
    password: str

    @validator('cpf')
    def validate_cpf(cls, value):
        if not is_cpf_valid(value):
            raise ValueError('Invalid CPF')

        return value

    class Config:
        allow_mutation = False
