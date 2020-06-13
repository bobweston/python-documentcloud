# Future
from __future__ import division, print_function, unicode_literals

# Third Party
from future.utils import python_2_unicode_compatible

# Local
from .base import BaseAPIClient, BaseAPIObject


@python_2_unicode_compatible
class Organization(BaseAPIObject):
    """A documentcloud organization"""

    api_path = "organizations"
    writable_fields = []

    def __str__(self):
        return self.name


class OrganizationClient(BaseAPIClient):
    """Client for interacting with organizations"""

    api_path = "organizations"
    resource = Organization
