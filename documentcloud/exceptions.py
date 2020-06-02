"""
Custom exceptions for python-documentcloud
"""


class DocumentCloudError(Exception):
    """Base class for errors for python-documentcloud"""

    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        if response:
            json = response.json()
            self.error = json.get('error')
            self.status_code = response.status_code
        else:
            self.error = None
            self.status_code = None
        super().__init__(self, *args, **kwargs)


class DoesNotExistError(DocumentCloudError):
    """Raised when the user asks the API for something it cannot find"""


class MultipleObjectsReturnedError(DocumentCloudError):
    """Raised when the API returns multiple objects when it expected one"""


class APIError(DocumentCloudError):
    """Any other error calling the API"""
