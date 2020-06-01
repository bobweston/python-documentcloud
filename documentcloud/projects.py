from .base import BaseAPIClient, BaseAPIObject
from .documents import Document
from .toolbox import get_id


class Project(BaseAPIObject):
    """A documentcloud project"""

    api_path = "projects"
    writable_fields = ["description", "private", "title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._document_list = None

    def __str__(self):
        return self.title

    def save(self):
        """Add the documents to the project as well"""
        super().save()
        if self._document_list:
            data = [{'document': d} for d in self.document_ids]
            response = self._client.put(f"{self.api_path}/{self.id}/documents/", json=data)
            response.raise_for_status()

    @property
    def document_list(self):
        # XXX error checking ala DocumentSet ???
        if self._document_list is None:
            # XXX paginate
            response = self.client.get(f"{self.api_path}/{get_id(self.id)}/documents/")
            response.raise_for_status()
            self._document_list = [
                Document(self._client, r) for r in response.json()["results"]
            ]
        return self._document_list

    @document_list.setter
    def document_list(self, value):
        # XXX validation ??
        self._document_list = value

    @property
    def document_ids(self):
        return [d.id for d in self.document_list]



class ProjectClient(BaseAPIClient):
    """Client for interacting with projects"""

    api_path = "projects"
    resource = Project

    # XXX get by title

    def create(self, title, description="", document_ids=None):
        data = {"title": title, "description": description}
        response = self._client.post(f"{self.api_path}/", json=data)
        response.raise_for_status()
        return Project(self.client, response.json())

    def get_or_create_by_title(self, title):
        # XXX need better way of detecting non existent resources
        try:
            project = self.get(title=title)
            created = False
        except:  # XXX DoesNotExist
            project = self.create(title=title)
            created = True
        return project, created
