import json
class response:
    def __init__(self, status, data):
        self._response = {}
        self._response['status'] = status
        self._response.update(data)

    def __str__(self):
        return json.dumps(self._response)
