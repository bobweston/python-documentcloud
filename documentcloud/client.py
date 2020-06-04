"""
The public interface for the DocumentCloud API
"""

import logging
from functools import partial

import requests

from .documents import DocumentClient
from .exceptions import APIError
from .organizations import OrganizationClient
from .projects import ProjectClient
from .toolbox import CredentialsFailedError, requests_retry_session
from .users import UserClient

BASE_URI = "https://api.beta.documentcloud.org/api/"
AUTH_URI = "https://accounts.muckrock.com/api/"
TIMEOUT = 10

logger = logging.getLogger("documentcloud")


class DocumentCloud:
    """
    The public interface for the DocumentCloud API
    """

    def __init__(
        self,
        username=None,
        password=None,
        base_uri=BASE_URI,
        auth_uri=AUTH_URI,
        timeout=TIMEOUT,
        loglevel=None,
    ):
        self.base_uri = base_uri
        self.auth_uri = auth_uri
        self.username = username
        self.password = password
        self._user_id = None
        self.timeout = timeout
        self.refresh_token = None
        self.session = requests.Session()
        self._set_tokens()

        if loglevel:
            logging.basicConfig(
                level=loglevel,
                format="%(asctime)s %(levelname)-8s %(name)-25s %(message)s",
            )
        else:
            logger.addHandler(logging.NullHandler())

        self.documents = DocumentClient(self)
        self.projects = ProjectClient(self)
        self.users = UserClient(self)
        self.organizations = OrganizationClient(self)

    def _set_tokens(self):
        """Set the refresh and access tokens"""
        if self.refresh_token:
            access_token, self.refresh_token = self._refresh_tokens(self.refresh_token)
        elif self.username and self.password:
            access_token, self.refresh_token = self._get_tokens(
                self.username, self.password
            )
        else:
            access_token = None

        if access_token:
            self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def _get_tokens(self, username, password):
        """Get an access and refresh token in exchange for the username and password"""
        response = requests_retry_session().post(
            f"{self.auth_uri}token/",
            json={"username": username, "password": password},
            timeout=self.timeout,
        )

        if response.status_code == requests.codes.UNAUTHORIZED:
            raise CredentialsFailedError("The username and password is incorrect")

        self.raise_for_status(response)

        json = response.json()
        return (json["access"], json["refresh"])

    def _refresh_tokens(self, refresh_token):
        """Refresh the access and refresh tokens"""
        response = requests_retry_session().post(
            f"{self.auth_uri}refresh/",
            json={"refresh": refresh_token},
            timeout=self.timeout,
        )

        if response.status_code == requests.codes.UNAUTHORIZED:
            # refresh token is expired
            return self._get_tokens(self.username, self.password)

        self.raise_for_status(response)

        json = response.json()
        return (json["access"], json["refresh"])

    @property
    def user_id(self):
        if self._user_id is None:
            user = self.users.get("me")
            self._user_id = user.id
        return self._user_id

    def _request(self, method, url, raise_error=True, **kwargs):
        """Generic method to make API requests"""
        logger.info("request: %s - %s - %s", method, url, kwargs)
        set_tokens = kwargs.pop("set_tokens", True)
        full_url = kwargs.pop("full_url", False)

        if not full_url:
            url = f"{self.base_uri}{url}"

        response = requests_retry_session(session=self.session).request(
            method, url, timeout=self.timeout, **kwargs
        )
        logger.debug("response: %s - %s", response.status_code, response.content)
        if response.status_code == requests.codes.FORBIDDEN and set_tokens:
            self._set_tokens()
            # track set_tokens to not enter an infinite loop
            kwargs["set_tokens"] = False
            return self._request(method, url, **kwargs)

        if raise_error:
            self.raise_for_status(response)

        return response

    def __getattr__(self, attr):
        """Generate methods for each HTTP request type"""
        methods = ["get", "options", "head", "post", "put", "patch", "delete"]
        if attr in methods:
            return partial(self._request, attr)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{attr}'"
        )

    def raise_for_status(self, response):
        """Raise for status with a custom error class"""
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise APIError(response=exc.response)
