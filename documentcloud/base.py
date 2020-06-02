
from dateutil.parser import parse as dateparser

from .toolbox import get_id


class BaseAPIClient:
    """Base client for all API resources"""

    # subclasses should set these
    api_path = None
    resource = None

    def __init__(self, client):
        self.client = client

    def get(self, id_):
        """Get a resource by its ID"""
        response = self.client.get(f"{self.api_path}/{get_id(id_)}/")
        return self.resource(self.client, response.json())

    def delete(self, id):
        """Deletes a resource"""
        self.client.delete(f"{self.api_path}/{get_id(id)}/")

    def all(self):
        return self.list()

    def list(self, page=1, per_page=None):
        # XXX custom list class to show metadata? (next_url/prev_url/count etc)
        params = {'page': page}
        if per_page is not None:
            params['per_page'] = per_page
        response = self.client.get(f"{self.api_path}/", params=params)
        return [self.resource(self.client, r) for r in response.json()["results"]]


class BaseAPIObject:
    """Base object for all API resources"""

    date_fields = []

    def __init__(self, client, dict_):
        self.__dict__ = dict_
        self._client = client
        for field in self.date_fields:
            setattr(self, field, dateparser(getattr(self, field)))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def put(self):
        """Alias for save"""
        return self.save()

    def save(self):
        data = {f: getattr(self, f) for f in self.writable_fields if hasattr(self, f)}
        self._client.put(f"{self.api_path}/{self.id}/", json=data)

    def delete(self):
        self._client.delete(f"{self.api_path}/{self.id}/")
