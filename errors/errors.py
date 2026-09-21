class ApplicationError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    @staticmethod
    def code_to_message():
        pass