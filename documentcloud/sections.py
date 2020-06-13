# Future
from __future__ import division, print_function, unicode_literals

# Third Party
from future.utils import python_2_unicode_compatible

# Local
from .base import BaseAPIObject, ChildAPIClient
from .toolbox import merge_dicts


@python_2_unicode_compatible
class Section(BaseAPIObject):
    """A section of a document"""

    writable_fields = ["page_number", "title"]

    def __str__(self):
        return "{} - p{}".format(self.title, self.page)

    @property
    def api_path(self):
        return "documents/{}/sections".format(self.document.id)

    @property
    def page(self):
        return self.page_number


class SectionClient(ChildAPIClient):
    """Client for interacting with Sections"""

    resource = Section

    @property
    def api_path(self):
        return "documents/{}/sections".format(self.parent.id)

    def create(self, title, page_number):
        data = {"title": title, "page_number": page_number}
        response = self.client.post(self.api_path + "/", json=data)
        return Section(
            self.client, merge_dicts(response.json(), {"document": self.parent})
        )
