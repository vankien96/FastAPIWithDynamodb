
class UnAuthorizeException(Exception):
    pass

class BadRequestException(Exception):
    def __init__(self, name: str):
        self.name = name