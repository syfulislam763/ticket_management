class UnicornException(Exception):
    def __init__(self, msg:str):
        self.msg = msg


class UnicornBadException(Exception):
    def __init__(self, msg:str):
        self.msg = msg

class UnicornTicketException(Exception):
    def __init__(self, code:int, msg:str):
        self.msg = msg
        self.code = code