import requests
import json
from abc import ABC


class BackendRest(ABC):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

    def __init__(self, _baseurl_):
        self.session = requests.Session()
        self.baseurl = _baseurl_

    @staticmethod
    def get_request_results(request_response):
        # Need to check if the response text is on JSON format
        try:
            parsedJSON = json.loads(request_response.text)
        except Exception as e:
            parsedJSON = {}

        result = {
            "response": request_response,
            "parsedResponse": parsedJSON
        }

        return result
