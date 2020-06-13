# Future
from __future__ import division, print_function, unicode_literals

# Third Party
from future.utils import python_2_unicode_compatible

# Local
from .base import BaseAPIClient, BaseAPIObject


@python_2_unicode_compatible
class User(BaseAPIObject):
    """A documentcloud user"""

    api_path = "users"
    writable_fields = ["organization"]

    def __str__(self):
        return self.username


class UserClient(BaseAPIClient):
    """Client for interacting with users"""

    api_path = "users"
    resource = User
