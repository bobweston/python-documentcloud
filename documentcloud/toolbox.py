"""
A few toys the API will use.
"""
import time
from functools import wraps
from itertools import zip_longest
from urllib.parse import urlparse

import requests
import six
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

#
# Exceptions
#


class CredentialsMissingError(Exception):
    """
    Raised if an API call is attempted without the required login credentials
    """

    pass


class CredentialsFailedError(Exception):
    """
    Raised if an API call fails because the login credentials are no good.
    """

    pass


class DoesNotExistError(Exception):
    """
    Raised when the user asks the API for something it cannot find.
    """

    pass


class DuplicateObjectError(Exception):
    """
    Raised when the user tries to add a duplicate to a distinct list.
    """

    pass


#
# Decorators
#


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


# XXX remove
def retry(ExceptionToCheck, tries=3, delay=2, backoff=2):
    """
    Retry decorator published by Saltry Crane.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try_one_last_time = True
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                    try_one_last_time = False
                    break
                except ExceptionToCheck:
                    six.print_("Retrying in %s seconds" % str(mdelay))
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            if try_one_last_time:
                return f(*args, **kwargs)
            return

        return f_retry  # true decorator

    return deco_retry


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
    New style: 123
    """

    if isinstance(id_, int):
        return id_
    elif "-" in id_:
        return id_.split("-")[0]
    else:
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
