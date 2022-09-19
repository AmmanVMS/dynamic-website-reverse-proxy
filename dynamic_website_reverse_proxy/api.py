"""The API that is provided by the JSON endpoint.
"""
from http import HTTPStatus
from .full_website import FullWebsite
import sys
import re
from urllib.parse import urlparse
import ipaddress

VALID_DOMAIN = re.compile("^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
VALID_IPV4 = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")


def catch_and_respond(function):
    """Make a response when an error occurs."""
    def wrapped(*args, **kw):
        try:
            return function(*args, **kw)
        except:
            ty, err, tb = sys.exc_info()
            return {
                "status": HTTPStatus.BAD_REQUEST,
                "error": {
                    "type": ty.__name__,
                    "message": str(err),
                }
            }
    return wrapped


class IncompleteRequestData(ValueError):
    """The request data misses information."""
    def __init__(self, field):
        self.field = field
        super().__init__(f"The field '{field}' is missing.")


class APIv1:
    """This represents the API version 1"""

    def __init__(self, database, config):
        """Serve the database with a configuration through the API."""
        self._db = database
        self._config = config

    @catch_and_respond
    def create_website(self, user, data):
        """Create a website as a user with certain data in it."""
        for field in ("domain", "source"):
            if not isinstance(data.get(field), str):
                raise IncompleteRequestData(field)
        if not VALID_DOMAIN.match(data["domain"]):
            raise ValueError("The field 'domain' must be a valid domain name.")
        source = urlparse(data["source"])
        if source[0] not in ("http", "https"):
            raise ValueError("The field 'source' must be a valid http/https url.")
        if not VALID_IPV4.match(source.hostname) or ipaddress.ip_address(source.hostname) not in self._config.network:
            raise ValueError(f"The field 'source' must be inside {self._config.network}.")
        website = FullWebsite(data["source"], data["domain"], self._config)
        website.change_owner_to(user)
        self._db.add_website(website)
        return {
            "status": HTTPStatus.CREATED,
            "data": {
                "type": "website",
                "source": data["source"],
                "domain": data["domain"],
                "owner" : user.id
            }
        }
