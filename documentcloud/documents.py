"""
Documents
"""

from .toolbox import credentials_required, get_id


class DocumentClient:
    """Client for interacting with Documents"""

    def __init__(self, client):
        self.client = client

    def search(self, query, page=1, per_page=100, mentions=3, data=False):
        """Return documents matching a search query"""
        response = self.client.get(
            "documents/search/", params={"q": query, "page": page, "per_page": per_page}
        )
        response.raise_for_status()
        return [Document(self, d) for d in response.json()["results"]]

    def get(self, id_):
        """Get a document by its ID"""
        response = self.client.get(f"documents/{get_id(id_)}/")
        response.raise_for_status()
        return Document(self, response.json())

    @credentials_required
    def upload(self, pdf, **kwargs):
        """
        title=None,
        source=None,
        description=None,
        related_article=None,
        published_url=None,
        access="private",
        project=None,
        data=None,
        secure=False,
        force_ocr=False,
        """

    @credentials_required
    def upload_directory(self, path, **kwargs):
        """
        source=None,
        description=None,
        related_article=None,
        published_url=None,
        access="private",
        project=None,
        data=None,
        secure=False,
        force_ocr=False,
        """

    @credentials_required
    def delete(self, id_):
        """Deletes a document"""
        response = self.client.delete(f"documents/{get_id(id_)}/")
        response.raise_for_status()


class Document:
    """A single DocumentCloud document"""

    def __init__(self, client, dict_):
        self.__dict__ = dict_
        self._client = client

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)

    def __str__(self):
        return self.title

    def save(self):
        pass

    def put(self):
        """Alias for save"""
        return self.save()

    def delete(self):
        """Delete this document"""
        self._client.delete(self.id)
