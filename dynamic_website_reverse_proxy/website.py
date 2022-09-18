"""A website to serve."""
from .base_website import BaseWebsite

class Website(BaseWebsite):
    """This is a website registered in the proxy as a sub domain."""

    def __init__(self, source_url, sub_domain, config):
        """Create a new website served under a subdomain.

        - source_url - the url of the source
        - sub_domain - the first part of the domain
        - config - an object with the attributes
            - http_port
            - domain
        """
        super().__init__(source_url, config)
        self._sub_domain = sub_domain

    @property
    def sub_domain(self):
        """The subdomain part of the proxy domain."""
        return self._sub_domain

    @property
    def domain(self):
        """The domain name to serve the content."""
        return self.sub_domain + "." + self._config.domain

    def can_be_edited(self):
        """Whether the user can edit the website."""
        return True
