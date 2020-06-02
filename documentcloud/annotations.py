from listcrunch.listcrunch import uncrunch

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
        return f"documents/{self.document.id}/notes"

    @property
    def location(self):
        page_spec = uncrunch(self.document.page_spec)
        width, height = page_spec[self.page_number].split('x')
        width, height = float(width), float(height)
        # normalize to a width of 700
        height = (700 / width) * height
        width = 700
        return Location(
            int(self.y1 * height),
            int(self.x2 * width),
            int(self.y2 * height),
            int(self.x1 * width),
        )


class Location:
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
