"""The API that is provided by the JSON endpoint.
"""
from http import HTTPStatus
from .full_website import FullWebsite
from .website import Website
import sys
import re
from urllib.parse import urlparse
import ipaddress
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, SYSTEM, User
from io import StringIO
import traceback


VALID_DOMAIN = re.compile("^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9-]*[A-Za-z0-9])$")
VALID_IPV4 = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")


def catch_and_respond(function):
    """Make a response when an error occurs."""
    def wrapped(*args, **kw):
        try:
            return function(*args, **kw)
        except:
            ty, err, tb = sys.exc_info()
            file = StringIO()
            traceback.print_exception(ty, err, tb, file=file)
            tb_string = file.getvalue()
            print(tb_string) # for tests
            return {
                "status": getattr(err, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
                "error": {
                    "type": ty.__name__,
                    "message": str(err),
                    "traceback": tb_string,
                }
            }
    return wrapped


class BadRequestError(ValueError):
    """The request does not look ok."""
    http_status = HTTPStatus.BAD_REQUEST


class IncompleteRequestData(BadRequestError):
    """The request data misses information."""
    def __init__(self, field):
        self.field = field
        super().__init__(f"The field '{field}' is missing.")


class PermissionDenied(PermissionError):
    """This request requires other permissions."""
    http_status = HTTPStatus.UNAUTHORIZED
    def __init__(self, action):
        self.action = action
        super().__init__(action.as_denied_permission())


class InvalidUserName(ValueError):
    """This user name can not be used."""
    http_status = HTTPStatus.NOT_ACCEPTABLE

    def __init__(self, username):
        """Create a new error for a username."""
        super().__init__(f"You can not use the name '{username}' on this system.")
    

class InvalidLogin(ValueError):
    """Wrong username or password."""
    http_status = HTTPStatus.UNAUTHORIZED


class APIv1:
    """This represents the API version 1"""

    def __init__(self, database, config):
        """Serve the database with a configuration through the API."""
        self._db = database
        self._config = config

    def validate_website_data(self, data):
        """Raise an error if the data is invalid."""
        for field in ("domain", "source"):
            if not isinstance(data.get(field), str):
                raise IncompleteRequestData(field)
        if not VALID_DOMAIN.match(data["domain"]):
            raise BadRequestError("The field 'domain' must be a valid domain name.")
        source = urlparse(data["source"])
        if source[0] not in ("http", "https"):
            raise BadRequestError("The field 'source' must be a valid http/https url.")
        if not VALID_IPV4.match(source.hostname) or ipaddress.ip_address(source.hostname) not in self._config.network:
            raise BadRequestError(f"The field 'source' must be inside {self._config.network}.")

    def check_if(self, action):
        """Check if an action is allowed and if not, raise an PermissionDenied."""
        if not self._config.permissions.allow(action):
            raise PermissionDenied(action)

    @catch_and_respond
    def create_website(self, credentials, data):
        """Create a website as a user identified by the credentials with certain data in it."""
        user = self.login(credentials)
        self.validate_website_data(data)
        domain = data["domain"]
        if domain.endswith("." + self._config.domain):
            website = Website(data["source"], domain[:-len(self._config.domain) - 1], self._config)
        else:
            website = FullWebsite(data["source"], domain, self._config)
        website.change_owner_to(user)
        self.check_if(user.can.create(website))
        self._db.proxy.add(website)
        return {
            "status": HTTPStatus.CREATED,
            "data": {
                "type": "website",
                "source": data["source"],
                "domain": data["domain"],
                "owner" : user.id
            }
        }

    def login(self, credentials):
        """Log in a user and see if they like to be returned."""
        if credentials == None:
            return ANONYMOUS
        username, password = credentials
        if username == SYSTEM.id or not username.isalnum():
            raise InvalidUserName(username)
        is_admin = password == self._config.admin_password and password != ""
        if username == ADMIN.id:
            if not is_admin:
                raise InvalidUserName(username)
            return ADMIN
        for user in self._db.proxy.users:
            if user.id == username:
                if is_admin or user.is_password(password):
                    return user
                raise InvalidLogin()
        return User(username, password)
