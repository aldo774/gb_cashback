import logging


def _can_be_handle(data, field):
    return isinstance(data, dict) and data.get(field) and isinstance(data.get(field), str)

class HideDocument(logging.Filter):
    def filter(self, record):
        if _can_be_handle(record.args, 'cpf'):
            cpf = record.args['cpf']
            record.args['cpf'] = f'{cpf[:4] :*<11}'

        return True

class HideEmail(logging.Filter):
    def filter(self, record):
        if _can_be_handle(record.args, 'email'):
            email = record.args['email']
            email_parts = email.split('@')

            record.args['email'] = f'{email_parts[0][:5] :*<10}{email_parts[1][-3:]}'

        return True

class HideName(logging.Filter):
    def filter(self, record):
        if _can_be_handle(record.args, 'name'):
            name = record.args['name']
            name_parts = name.split(' ')

            record.args['name'] = f'{name_parts[0]} {name_parts[1][3:] :*<5}'

        return True

class HidePassword(logging.Filter):
    def filter(self, record):
        if _can_be_handle(record.args, 'pasword'):
            record.args['password'] = '**************'

        return True
