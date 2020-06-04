"""
A few toys the API will use.
"""
from functools import wraps
from itertools import zip_longest
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

#
# Decorators
#


# XXX keep?
def credentials_required(method_func):
    """
    Decorator for methods that checks that the client has credentials.

    Throws a CredentialsMissingError when they are absent.
    """

    def _checkcredentials(self, *args, **kwargs):
        if self.username and self.password:
            return method_func(self, *args, **kwargs)
        else:
            raise CredentialsMissingError(
                "This is a private method. You must provide a username and "
                "password when you initialize the DocumentCloud client to attempt "
                "this type of request."
            )

    return wraps(method_func)(_checkcredentials)


#
# Utilities
#


def requests_retry_session(
    retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None
):
    """Automatic retries for HTTP requests
    See: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_id(id_):
    """Allow specifying old or new style IDs and convert old style to new style IDs

    Old style: 123-the-slug
    New style: 123 or the-slug-123
    """

    if isinstance(id_, int):
        return id_
    elif "-" in id_:
        front = id_.split("-", 1)[0]
        if front.isdigit():
            return front
        back = id_.rsplit("-", 1)[-1]
        if back.isdigit():
            return back

    return id_


def is_url(url):
    """Is `url` a valid url?"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
