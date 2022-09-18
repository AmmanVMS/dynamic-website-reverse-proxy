"""Configuration for the app

"""
import os

class Config:
    """User configuration of the app."""

    def __init__(self, environment):
        """Create a new Config objeict configured by an environment dictionary."""

    @property
    def here(self):
        """The location of the app"""
        return os.path.dirname(__file__ or ".")

    @property
    def static_files(self):
        """The location of the app static files to serve"""

    @property
    def domain(self):
        """The base domain for the requests."""

    @property
    def default_server(self):
        """The domain for the default server serve content for unknown host names."""

    @property
    def debug(self):
        """Whether to show more output when an error happens."""

    @property
    def database(self):
        """The database to store the user configuration in."""

    @property
    def app_port(self):
        """The port for the web app."""

    @property
    def http_port(self):
        """The port for http requests to nginx."""

    @property
    def maximum_host_name_length(self):
        """The maximum length of a host name entered by a user."""

    @property
    def source_code(self):
        """The directory with the source code."""


class EnvConfig(Config):
    """An environment configuration.

    Singleton.
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

