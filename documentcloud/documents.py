"""
Documents
"""

import os
import re
import warnings
from functools import partial

import requests

from .annotations import Annotation
from .base import BaseAPIClient, BaseAPIObject
from .organizations import OrganizationClient
from .toolbox import grouper, is_url
from .users import UserClient

BULK_LIMIT = 25


class Document(BaseAPIObject):
    """A single DocumentCloud document"""

    api_path = "documents"
    writable_fields = [
        "access",
        "data",
        "description",
        "language",
        "related_article",
        "published_url",
        "source",
        "title",
    ]
    date_fields = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None
        self._organization = None

    def __str__(self):
        return self.title

    def __getattr__(self, attr):
        """Generate methods for fetching resources"""
        p_image = re.compile(
            r"^get_(?P<size>thumbnail|small|normal|large)_image_url(?P<list>_list)?$"
        )
        get = attr.startswith("get_")
        url = attr.endswith("_url")
        text = attr.endswith("_text")
        # this allows dropping `get_` to act like a property, ie
        # .full_text_url
        if not get and hasattr(self, f"get_{attr}"):
            return getattr(self, f"get_{attr}")()
        # this allows dropping `_url` to fetch the url, ie
        # .get_full_text()
        if not url and hasattr(self, f"{attr}_url"):
            return lambda *a, **k: self._get_url(
                getattr(self, f"{attr}_url")(*a, **k), text
            )
        # this combines both of the above, ie
        # .full_text
        if not get and not url and hasattr(self, f"get_{attr}_url"):
            return lambda *a, **k: self._get_url(
                getattr(self, f"{attr}_url")(*a, **k), text
            )()
        # this genericizes the image sizes
        m_image = p_image.match(attr)
        if m_image and m_image.group("list"):
            return partial(self.get_image_url_list, size=m_image.group("size"))
        if m_image and not m_image.group("list"):
            return partial(self.get_image_url, size=m_image.group("size"))
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{attr}'"
        )

    def __dir__(self):
        attrs = super().__dir__()
        getters = [a for a in attrs if a.startswith("get_")]
        attrs += [a[len("get_") :] for a in getters]
        attrs += [a[: -len("_url")] for a in getters if a.endswith("url")]
        attrs += [a[len("get_") : -len("_url")] for a in getters if a.endswith("url")]
        for size in ["thumbnail", "small", "normal", "large"]:
            attrs += [
                f"get_{size}_image_url",
                f"{size}_image_url",
                f"get_{size}_image",
                f"{size}_image",
                f"get_{size}_image_url_list",
                f"{size}_image_url_list",
            ]
        return attrs

    @property
    def pages(self):
        return self.page_count

    @pages.setter
    def pages(self, value):
        self.page_count = value

    @property
    def annotations(self):
        response = self._client.get(f"documents/{self.id}/notes/")
        response.raise_for_status()
        return [
            Annotation(self._client, {**a, "document": self.id})
            for a in response.json()["results"]
        ]

    @property
    def sections(self):
        response = self._client.get(f"documents/{self.id}/sections/")
        response.raise_for_status()
        return [
            Section(self._client, {**a, "document": self.id})
            for a in response.json()["results"]
        ]

    @property
    def mentions(self):
        if hasattr(self, "highlights"):
            return [Mention(page, text) for page, text in self.highlights.items()]
        else:
            return []

    @property
    def canonical_url(self):
        return f"{self._client.base_uri}documents/{self.id}-{self.slug}"

    # XXX expose a nicer interface for getting the user/org objects
    # XXX expose a way to preload user/org object using expand
    # XXX expose a public search url for user/org when available
    def _load_user(self):
        if not self._user:
            self._user = UserClient(self._client).get(self.user)

    def _load_organization(self):
        if not self._organization:
            self._organization = OrganizationClient(self._client).get(self.organization)

    @property
    def contributor(self):
        self._load_user()
        return self._user.name

    @property
    def contributor_organization(self):
        self._load_organization()
        return self._organization.name

    @property
    def contributor_organization_slug(self):
        self._load_organization()
        return self._organization.slug

    def _get_url(self, url, text):
        if self.access == "public":
            response = requests.get(
                url, headers={"User-Agent": "python-documentcloud2"}
            )
            response.raise_for_status()
            if text:
                return response.content.decode("utf8")
            else:
                return response.content
        else:
            raise NotImplementedError(
                "Currently, DocumentCloud only allows you to access this resource "
                "on public documents."
            )

    # Resource URLs
    def get_full_text_url(self):
        return f"{self.asset_url}documents/{self.id}/{self.slug}.txt"

    def get_page_text_url(self, page=1):
        return f"{self.asset_url}documents/{self.id}/pages/{self.slug}-p{page}.txt"

    def get_json_text_url(self):
        return f"{self.asset_url}documents/{self.id}/{self.slug}.txt.json"

    def get_pdf_url(self):
        return f"{self.asset_url}documents/{self.id}/{self.slug}.pdf"

    def get_image_url(self, page=1, size="normal"):
        return (
            f"{self.asset_url}documents/{self.id}/pages/"
            f"{self.slug}-p{page}-{size}.gif"
        )

    def get_image_url_list(self, size="normal"):
        return [
            self.get_image_url(page=i, size=size) for i in range(1, self.page_count + 1)
        ]


class DocumentClient(BaseAPIClient):
    """Client for interacting with Documents"""

    api_path = "documents"
    resource = Document

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
            "data",
            "force_ocr",
            "projects",
        ]
        # these parameters currently do not work, investigate...
        ignored_parameters = ["secure"]

        # title is required, so set a default
        params = {"title": self._get_title(name)}

        if "project" in kwargs:
            params["projects"] = [kwargs["project"]]

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
        force_ocr = kwargs.pop("force_ocr", False)
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
        response = self.client.post(
            f"documents/{doc_id}/process/", json={"force_ocr": force_ocr}
        )
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


class Mention:
    """A snipper from a document search"""

    def __init__(self, page, text):
        if page.startswith("page_no_"):
            page = page[len("page_no_") :]
        self.page = page
        self.text = text


class Section(BaseAPIObject):
    """A section of a document"""

    writable_fields = [
        "page_number",
        "title",
    ]

    def __str__(self):
        return f"{self.title} - p{self.page}"

    @property
    def api_path(self):
        return f"documents/{self.document}/sections"

    @property
    def page(self):
        return self.page_number
