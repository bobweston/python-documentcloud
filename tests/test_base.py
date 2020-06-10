# Third Party
import pytest

# DocumentCloud
from documentcloud.exceptions import DuplicateObjectError


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

    def test_append_bad_type(self, project):
        with pytest.raises(TypeError):
            project.document_list.append(1)

    def test_append_dupes(self, project, document):
        with pytest.raises(DuplicateObjectError):
            project.document_list.append(document)
