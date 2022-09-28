"""Configuration for the app

"""
import os
import ipaddress
from .default_website import DefaultWebsite
from .full_website import FullWebsite
from .permissions import Permissions


class Config:
    """User configuration of the app."""

    def __init__(self, environment):
        """Create a new Config objeict configured by an environment dictionary."""
        self._env = environment

    @property
    def here(self):
        """The location of the app."""
        return os.path.dirname(__file__ or ".")

    @property
    def static_files(self):
        """The location of the app static files to serve."""
        return os.path.join(self.here, "static")

    @property
    def template_lookup(self):
        """The location of the app template files to serve.
        
        This replaces the template_lookup key word argument and
        the TEMPLATE_PATH global variable of bottle.
        """
        return [os.path.join(self.here, "templates")]

    @property
    def nginx_conf(self):
        """The location of the configuration file for nginx."""
        return self._env.get("NGINX_CONF", "/tmp/nginx.conf")

    @property
    def domain(self):
        """The base domain for the requests."""
        return self._env.get("DOMAIN", f"localhost:{self.app_port}")

    @property
    def default_server(self):
        """The domain for the default server serve content for unknown host names."""
        url = self._env.get("DEFAULT_SERVER")
        if not url:
            url = f"localhost:{self.app_port}"
        if not url.startswith("http://") and not url.startswith("https://") :
            url = "http://" + url
        return url

    @property
    def debug(self):
        """Whether to show more output when an error happens."""
        return self._env.get("DEBUG", "").lower() != "false" 

    @property
    def database(self):
        """The database to store the user configuration in."""
        location = self._env.get("DATABASE", "")
        from .database import NullDatabase, Database
        if not location:
            return NullDatabase()
        return Database(location)

    @property
    def app_port(self):
        """The port for the web app."""
        return int(self._env.get("PORT", 9001))

    @property
    def http_port(self):
        """The port for http requests to nginx."""
        return int(self._env.get("HTTP_PORT", 80))

    @property
    def maximum_host_name_length(self):
        """The maximum length of a host name entered by a user."""
        return int(self._env.get("MAXIMUM_HOST_NAME_LENGTH", 50))

    @property
    def source_code(self):
        """The directory with the source code."""
        return self._env.get("SOURCE_CODE", self.here)

    @property
    def network(self):
        """The network to choose ip addresses from that are targets."""
        return ipaddress.ip_network(self._env.get("NETWORK", "10.0.0.0/8"))

    @property
    def websites(self):
        """A list of websites configured by the environment."""
        websites = [DefaultWebsite(self.default_server, self)]
        spec = self._env.get("DEFAULT_DOMAINS", "")
        for entry in spec.split(","):
            if not entry:
                continue
            domain, source = entry.split("->")
            domain = domain.strip()
            source = source.strip()
            websites.append(FullWebsite(source, domain, self))
        return websites

    @property
    def permissions_file(self):
        """The file where the permissions are stored."""
        return self._env.get("PERMISSIONS", os.path.join(self.here, "permissions.txt"))
        
    @property
    def permissions(self):
        """The permissions of this system."""
        permissions = []
        with open(self.permissions_file) as f:
            for line in f:
                permission = line[:line.find("#")].strip()
                if not permission:
                    continue
                permissions.append(permission)
        return Permissions(permissions)


class EnvConfig(Config):
    """An environment configuration.

    Singleton. Use from_environment().
    """

    def __init__(self):
        """Create a new config from the environment."""
        super().__init__(os.environ)

    def __reduce__(self):
        return "CONFIG"


CONFIG = EnvConfig()

def from_environment():
    """The configuration loaded from environment variables."""
    return CONFIG

