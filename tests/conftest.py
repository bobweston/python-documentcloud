import time

import pytest

from documentcloud.client import DocumentCloud

# Test against a development environment documentcloud instance
BASE_URI = "http://api.dev.documentcloud.org/api/"
AUTH_URI = "http://dev.squarelet.com/api/"
USERNAME = "test-user"
PASSWORD = "test-password"
TIMEOUT = 1.0


def _client():
    return DocumentCloud(
        username=USERNAME,
        password=PASSWORD,
        base_uri=BASE_URI,
        auth_uri=AUTH_URI,
        timeout=TIMEOUT,
    )


@pytest.fixture
def client():
    return _client()


@pytest.fixture
def public_client():
    return DocumentCloud(base_uri=BASE_URI, auth_uri=AUTH_URI, timeout=TIMEOUT)


@pytest.fixture(scope="module")
def document(project):
    client_ = _client()
    document_ = client_.documents.upload(
        "https://assets.documentcloud.org/documents/20071460/test.pdf",
        access="private",
        data={"_tag": ["document"]},
        description="A simple test document",
        source="DocumentCloud",
        related_article="https://www.example.com/article/",
        published_url="https://www.example.com/article/test.pdf",
        projects=[project.id],
    )
    # wait for document to finish processing
    # XXX how to vcr this
    while document_.status in ("nofile", "pending"):
        time.sleep(1)
        document_ = client_.documents.get(document_.id)
    assert document_.status == "success"

    return document_

@pytest.fixture(scope="module")
def project():
    client_ = _client()
    return client_.projects.create("Test Project", "This is a project for testing")
