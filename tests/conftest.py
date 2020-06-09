# Standard Library
import time

# Third Party
import pytest
import vcr

# DocumentCloud
from documentcloud.client import DocumentCloud

# Test against a development environment documentcloud instance
BASE_URI = "http://api.dev.documentcloud.org/api/"
AUTH_URI = "http://dev.squarelet.com/api/"
USERNAME = "test-user"
PASSWORD = "test-password"
TIMEOUT = 1.0


# We want to enable VCR for all tests
def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.vcr(match_on=["method", "uri", "body", "headers"]))


@pytest.fixture(scope="session")
@vcr.use_cassette("tests/cassettes/fixtures/client.yaml")
def client():
    return DocumentCloud(
        username=USERNAME,
        password=PASSWORD,
        base_uri=BASE_URI,
        auth_uri=AUTH_URI,
        timeout=TIMEOUT,
    )


@pytest.fixture
def public_client():
    return DocumentCloud(base_uri=BASE_URI, auth_uri=AUTH_URI, timeout=TIMEOUT)


def _wait_document(document, client, record_mode):
    # wait for document to finish processing
    while document.status in ("nofile", "pending"):
        if record_mode == "all":
            time.sleep(1)
        document = client.documents.get(document.id)
    assert document.status == "success"
    return document


@pytest.fixture(scope="session")
@vcr.use_cassette("tests/cassettes/fixtures/document.yaml")
def document(project, client, record_mode):
    document = client.documents.upload(
        "https://assets.documentcloud.org/documents/20071460/test.pdf",
        access="private",
        data={"_tag": ["document"]},
        description="A simple test document",
        source="DocumentCloud",
        related_article="https://www.example.com/article/",
        published_url="https://www.example.com/article/test.pdf",
        projects=[project.id],
    )
    document = _wait_document(document, client, record_mode)
    return document


@pytest.fixture
def document_factory(client, record_mode):
    def make_document(*args, **kwargs):
        document = client.documents.upload(*args, **kwargs)
        document = _wait_document(document, client, record_mode)
        return document

    return make_document


@pytest.fixture(scope="session")
@vcr.use_cassette("tests/cassettes/fixtures/project.yaml")
def project(client):
    return client.projects.create("Test Project", "This is a project for testing")
