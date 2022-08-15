class EmailAlreadyExists(Exception):
    msg = 'Email already exists'

    def __init__(self, detail=None):
        self.detail = detail or self.msg


class DealerAlreadyExists(Exception):
    msg = 'Dealer already exists'

    def __init__(self, detail=None):
        self.detail = detail or self.msg


class InvalidDealerData(Exception):
    msg = 'Some field in dealer data is bad formatted'

    def __init__(self, detail=None):
        self.detail = detail or self.msg
