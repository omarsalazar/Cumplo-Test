import json


class MockRequestsResponse():
    def __init__(self, mock_response, status_code=200, ok=True):
        self.response = mock_response
        self.status_code = status_code

    def json(self):
        return json.loads(self.response)


def mocked_validate_date_true(*args, **kwargs):
    return True


def mocked_get_banxico_data(*args, **kwargs):
    return {}


def mocked_validate_date_false(*args, **kwargs):
    return False


def mocked_currency_report(*args, **kwargs):
    return {}
