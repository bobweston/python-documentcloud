# Third Party
import pytest

# DocumentCloud
from documentcloud.documents import Document
from documentcloud.exceptions import DuplicateObjectError


def test_api_results(client):

    results = client.documents.list(per_page=2)
    assert isinstance(results[0], Document)
    assert len(results) > 0
    for doc in results:
        assert isinstance(doc, Document)


class TestAPISet:
    def test_init(self, project_factory, document):
        project = project_factory()
        document_list = project.document_list
        project.document_list = [document]
        project.document_list = document_list

    def test_init_bad_types(self, project):
        with pytest.raises(TypeError):
            project.document_list = [1, 2, 3]

    def test_init_dupes(self, project, document):
        with pytest.raises(DuplicateObjectError):
            project.document_list = [document, document]

    def test_append(self, project, document_factory):
        document = document_factory()
        project.document_list.append(document)
        assert project.document_list[-1] == document
        project.document_list.remove(document)

    def test_append_bad_type(self, project):
        with pytest.raises(TypeError):
            project.document_list.append(1)

    def test_append_dupes(self, project, document):
        with pytest.raises(DuplicateObjectError):
            project.document_list.append(document)

    def test_add(self, project, document_factory):
        document = document_factory()
        project.document_list.add(document)
        assert document in project.document_list
        project.document_list.remove(document)

    def test_add_bad_type(self, project):
        with pytest.raises(TypeError):
            project.document_list.add(1)

    def test_add_dupe(self, project, document):
        assert document in project.document_list
        length = len(project.document_list)
        project.document_list.add(document)
        assert document in project.document_list
        assert len(project.document_list) == length

    def test_extend(self, project, document_factory):
        document = document_factory()
        project.document_list.extend([document])
        assert document == project.document_list[-1]
        project.document_list.remove(document)

    def test_extend_bad_type(self, project):
        with pytest.raises(TypeError):
            project.document_list.extend([1])

    def test_extend_dupe(self, project, document):
        with pytest.raises(DuplicateObjectError):
            project.document_list.extend([document])
