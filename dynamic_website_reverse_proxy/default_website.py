"""The Default website to display for unknown domain names.

"""
from .website import Website

DEFAULT_WEBSITE_ID = object()

class DefaultWebsite(Website):
    """The website served by default."""

    def __init__(self, source_url, config):
        """Create a default website to serve when the domain is not used."""
        super().__init__(source_url, None, config)

    @property
    def sub_domain(self):
        """A default website has no subdomain."""
        raise ValueError("A default website has no subdomain.")

    @property
    def domain(self):
        """Replaces the domain with the nginx wildcard for all other domains."""
        return "default_server"

    @property
    def id(self):
        """The id of the default website. There is only one."""
        return DEFAULT_WEBSITE_ID
