class DealerNotExists(Exception):
    msg = 'Dealer does not Exists'

    def __init__(self, detail=None):
        self.detail = detail or self.msg


class OrderAlreadyExists(Exception):
    msg = 'Order already exists'

    def __init__(self, detail=None):
        self.detail = detail or self.msg


class InvalidOrderData(Exception):
    msg = 'Some field in order data is bad formatted'

    def __init__(self, detail=None):
        self.detail = detail or self.msg
