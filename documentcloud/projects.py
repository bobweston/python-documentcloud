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

    def get_document(self, doc_id):
        response = self.client.get(
            f"{self.api_path}/{get_id(self.id)}/documents/{doc_id}"
        )
        return Document(self._client, response.json())

    # XXX all should return just my projects ??


class ProjectClient(BaseAPIClient):
    """Client for interacting with projects"""

    api_path = "projects"
    resource = Project

    def get(self, id=None, title=None):
        if id is not None and title is not None:
            raise ValueError(
                "You can only retrieve a Project by id or title, not by both"
            )
        elif id is None and title is None:
            raise ValueError("You must provide an id or a title to make a request.")

        if id is not None:
            return self.get_by_id(id)
        elif title is not None:
            return self.get_by_title(title)

    def get_by_id(self, id_):
        return super().get(id_)

    def get_by_title(self, title):
        response = self.client.get(f"{self.api_path}/", params={"title": title})
        json = response.json()
        if json["count"] == 0:
            raise DoesNotExistError()
        elif json["count"] > 1:
            raise MultipleObjectsReturnedError()

        return self.resource(self.client, json["results"][0])

    def create(self, title, description="", private=True, document_ids=None):
        data = {"title": title, "description": description, "private": private}
        response = self._client.post(f"{self.api_path}/", json=data)
        project = Project(self.client, response.json())
        if document_ids:
            data = [{"document": d} for d in document_ids]
            response = self._client.put(
                f"{self.api_path}/{project.id}/documents/", json=data
            )
            # XXX create document objects
        return project

    def get_or_create_by_title(self, title):
        # XXX need better way of detecting non existent resources
        try:
            project = self.get(title=title)
            created = False
        except:  # XXX DoesNotExist
            project = self.create(title=title)
            created = True
        return project, created
