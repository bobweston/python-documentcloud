"""
Documents
"""

import os
import warnings

import requests
from dateutil.parser import parse as dateparser

from .toolbox import get_id, grouper, is_url

BULK_LIMIT = 25


class DocumentClient:
    """Client for interacting with Documents"""

    def __init__(self, client):
        self.client = client

    def search(self, query, page=1, per_page=None, **kwargs):
        """Return documents matching a search query"""

        if "mentions" in kwargs:
            warnings.warn(
                "The `mentions` argument to `search` is deprecated, "
                "it will always include mentions from all pages now",
                DeprecationWarning,
            )
        if "data" in kwargs:
            warnings.warn(
                "The `data` argument to `search` is deprecated, "
                "it will always include data now",
                DeprecationWarning,
            )

        params = {}
        if query:
            params["q"] = query
        if page is not None:
            # XXX page=None used to get all, I dislike this...
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = self.client.get("documents/search/", params=params)
        response.raise_for_status()
        return [Document(self.client, d) for d in response.json()["results"]]

    def get(self, id_):
        """Get a document by its ID"""
        response = self.client.get(f"documents/{get_id(id_)}/")
        response.raise_for_status()
        return Document(self.client, response.json())

    def upload(self, pdf, **kwargs):
        """Upload a document"""
        # if they pass in a URL, use the URL upload flow
        if is_url(pdf):
            return self._upload_url(pdf, **kwargs)
        # otherwise use the direct file upload flow - determine if they passed
        # in a file or a path
        elif hasattr(pdf, "read"):
            try:
                size = os.fstat(pdf.fileno()).st_size
            except (AttributeError, OSError):
                size = 0
        else:
            size = os.path.getsize(pdf)
            pdf = open(pdf, "rb")

        # DocumentCloud's size limit is set to 501MB to give people a little leeway
        # for OS rounding
        if size >= 501 * 1024 * 1024:
            raise ValueError(
                "The pdf you have submitted is over the DocumentCloud API's 500MB "
                "file size limit. Split it into smaller pieces and try again."
            )

        return self._upload_file(pdf, **kwargs)

    def _format_upload_parameters(self, name, **kwargs):
        """Prepare upload parameters from kwargs"""
        allowed_parameters = [
            "access",
            "description",
            "language",
            "related_article",
            "published_url",
            "source",
            "title",
        ]
        # these parameters currently do not work, investigate...
        # XXX do project and data in separate calls?
        ignored_parameters = ["project", "data", "secure", "force_ocr"]

        # title is required, so set a default
        params = {"title": self._get_title(name)}

        for param in allowed_parameters:
            if param in kwargs:
                params[param] = kwargs[param]

        for param in ignored_parameters:
            if param in kwargs:
                warnings.warn(f"The parameter `{param}` is not currently supported")

        return params

    def _get_title(self, name):
        """Get the default title for a document from its path"""
        return name.split(os.sep)[-1].rsplit(".", 1)[0]

    def _upload_url(self, file_url, **kwargs):
        """Upload a document from a publicly accessible URL"""
        params = self._format_upload_parameters(file_url, **kwargs)
        params["file_url"] = file_url
        response = self.client.post(f"documents/", json=params)
        response.raise_for_status()
        return Document(self.client, response.json())

    def _upload_file(self, file_, **kwargs):
        """Upload a document directly"""
        # create the document
        params = self._format_upload_parameters(file_.name, **kwargs)
        response = self.client.post("documents/", json=params)
        response.raise_for_status()

        # upload the file directly to storage
        create_json = response.json()
        presigned_url = create_json["presigned_url"]
        response = requests.put(presigned_url, data=file_.read())
        response.raise_for_status()

        # begin processing the document
        doc_id = create_json["id"]
        response = self.client.post(f"documents/{doc_id}/process/")
        response.raise_for_status()

        return Document(self.client, create_json)

    def upload_directory(self, path, **kwargs):
        """Upload all PDFs in a directory"""

        # do not set the same title for all documents
        kwargs.pop("title", None)

        # Loop through the path and get all the files
        path_list = []
        for (dirpath, _dirname, filenames) in os.walk(path):
            path_list.extend(
                [
                    os.path.join(dirpath, i)
                    for i in filenames
                    if i.lower().endswith(".pdf")
                ]
            )

        # Upload all the pdfs using the bulk API to reduce the number
        # of API calls and improve performance
        obj_list = []
        params = self._format_upload_parameters("", **kwargs)
        for pdf_paths in grouper(path_list, BULK_LIMIT):
            # Grouper will put None's on the end of the last group
            pdf_paths = [p for p in pdf_paths if p is not None]

            # create the documents
            response = self.client.post(
                "documents/",
                json=[{**params, "title": self._get_title(p)} for p in pdf_paths],
            )
            response.raise_for_status()

            # upload the files directly to storage
            create_json = response.json()
            obj_list.extend(create_json)
            presigned_urls = [j["presigned_url"] for j in create_json]
            for url, pdf_path in zip(presigned_urls, pdf_paths):
                response = requests.put(url, data=open(pdf_path, "rb").read())
                response.raise_for_status()

            # begin processing the documents
            doc_ids = [j["id"] for j in create_json]
            response = self.client.post("documents/process/", json={"ids": doc_ids})
            response.raise_for_status()

        # Pass back the list of documents
        return [Document(self.client, d) for d in obj_list]

    def delete(self, id_):
        """Deletes a document"""
        response = self.client.delete(f"documents/{get_id(id_)}/")
        response.raise_for_status()


class BaseAPIObject:
    def __init__(self, client, dict_):
        self.__dict__ = dict_
        self._client = client

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def put(self):
        """Alias for save"""
        return self.save()

    def save(self):
        data = {f: getattr(self, f) for f in self.writable_fields}
        response = self._client.put(f"{self.api_path}/{self.id}/", json=data)
        response.raise_for_status()

    def delete(self):
        response = self._client.delete(f"{self.api_path}/{self.id}/")
        response.raise_for_status()


class Document(BaseAPIObject):
    """A single DocumentCloud document"""

    # XXX put in backward compatibility shims for renamed fields
    # XXX deal with data

    api_path = "documents"
    writable_fields = [
        "access",
        "description",
        "language",
        "related_article",
        "published_url",  # XXX published_url
        "source",
        "title",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = dateparser(self.created_at)
        self.updated_at = dateparser(self.updated_at)

    def __str__(self):
        return self.title

    @property
    def annotations(self):
        response = self._client.get(f"documents/{self.id}/notes/")
        response.raise_for_status()
        return [
            Annotation(self._client, {**a, "document": self.id})
            for a in response.json()["results"]
        ]

    @property
    def canonical_url(self):
        return f"https://www.documentcloud.org/documents/{self.id}-{self.slug}"





class Annotation(BaseAPIObject):

    writable_fields = [
        "access",
        "content",
        "page_number",
        "title",
        "x1",
        "x2",
        "y1",
        "y2",
    ]

    def __str__(self):
        return self.title

    @property
    def api_path(self):
        return f"documents/{self.document}/notes"
