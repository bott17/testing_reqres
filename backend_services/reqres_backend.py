import datetime
from backend_services.backend_rest import BackendRest


class ReqResBackend(BackendRest):

    USERS_ENDPOINT = "users"
    REGISTER_ENDPOINT = "register"
    DOMAIN = "reqres.in/api"

    def __init__(self):
        super().__init__(f"https://{self.DOMAIN}")

    def users(self, method, payload=None, page=None, userID=None):

        url = f"{self.baseurl}/{self.USERS_ENDPOINT}"
        if userID is not None:
            url = f"{url}/{userID}"

        if page is not None:
            url = f"{url}?page={page}"

        response = self.session.request(method, url, json=payload)
        return self.get_request_results(response)

    def register(self, method, payload=None):

        url = f"{self.baseurl}/{self.REGISTER_ENDPOINT}"

        response = self.session.request(method, url, json=payload)
        return self.get_request_results(response)
