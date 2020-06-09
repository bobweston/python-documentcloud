# Third Party
import pytest

# DocumentCloud
from documentcloud.documents import Document
from documentcloud.exceptions import DoesNotExistError


class TestProject:
    def test_str(self, project):
        assert str(project) == project.title

    def test_save(self, client, project, document_factory):
        document = document_factory()
        assert document not in project.documents
        project.documents.append(document)
        project.save()
        project = client.projects.get(project.id)
        assert document in project.documents

    def test_document_list(self, project):
        assert len(project.document_list) > 0
        assert all(isinstance(d, Document) for d in project.document_list)

    def test_document_list_setter(self, client, project, document):
        assert document in project.document_list
        project.document_list = None
        assert document not in project.document_list
        project.document_list = [document]
        assert document in project.document_list

    def test_document_ids(self, project, document):
        assert document.id in project.document_ids

    def test_get_document(self, project, document):
        assert project.get_document(document.id)

    def test_get_document_missing(self, project, document_factory):
        document = document_factory()
        with pytest.raises(DoesNotExistError):
            project.get_document(document.id)


class TestProjectClient:

    def test_all(self, client):
        # XXX collaborators?
        pass

    def test_list(self, client):
        # XXX contrast to all
        assert client.projects.list()

    def test_get_id(self, client, project):
        assert client.projects.get(id=project.id)

    def test_get_title(self, client, project):
        assert client.projects.get(title=project.title)

    def test_get_nothing(self, client):
        with pytest.raises(ValueError):
            client.projects.get()

    def test_get_both(self, client, project):
        with pytest.raises(ValueError):
            client.projects.get(id=project.id, title=project.title)

    def test_get_by_id(self, client, project):
        assert client.projects.get_by_id(project.id)

    def test_get_by_title(self, client, project):
        assert client.projects.get_by_title(project.title)

    def test_get_or_create_by_title_get(self, client, project):
        title = project.title
        project, created = client.projects.get_or_create_by_title(title)
        assert project.title == title
        assert not created

    def test_get_or_create_by_title_create(self, client):
        title = "Created Title"
        project, created = client.projects.get_or_create_by_title(title)
        assert project.title == title
        project.delete()
        assert created
