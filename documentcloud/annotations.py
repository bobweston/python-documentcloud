from .base import BaseAPIObject


class Annotation(BaseAPIObject):
    """A note on a document"""

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

    @property
    def location(self):
        return Location(self.y1, self.x2, self.y2, self.x1)


class Location:
    # XXX convert to pixels using page spec? look at import code
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
