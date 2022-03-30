class BaseException(Exception):
    error: str
    status: int
    message: str

    def __init__(self, error: str, status: int, message: str) -> None:
        self.error = error
        self.status = status
        self.message = message

    def get_data(self):
        return {
            "error": self.error,
            "status": self.status,
            "message": self.message
        }


class SieApiInvalidDatesException(BaseException):
    pass


class SieApiInvalidCurrencyException(BaseException):
    pass


class SieApiBanxicoRequestException(BaseException):
    pass


class CommonException(BaseException):
    pass
