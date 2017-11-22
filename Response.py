# This class is an abstract wrapper for a response from any module of webSight #

import json


"""
    This class is an abstract interface wrapper for a response from any module of webSight.
    One must use this class as a return value of activating a module of webSight.
"""
class Response:
    """
    Response c-tor.

    Args:
        - status: boolean that is true iff the module succeed in its activation.
        - data: the actual data that the module emmited.
    
    Attributes:
        - (private) _response: a python's dictionary that contains the output data of that module.
    """
    def __init__(self, status, data):
        self._response = {}
        self._response['status'] = status
        self._response.update(data)
        
    """
    Returns string representation of that response, containing the module's ouytput data, and success status.
    """
    def __str__(self):
        return json.dumps(self._response)
