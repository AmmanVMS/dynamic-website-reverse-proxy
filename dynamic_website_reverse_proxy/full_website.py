"""Website serving without a subdomain.

"""
from .base_website import BaseWebsite


class FullWebsite(BaseWebsite):
    """A website just for a full domain, not a subdomain."""

    name_a_user_calls_me = "fqdn"

    def __init__(self, source, domain, config):
        """Create a new full domain serving website.
        
        The traffic will be served under the specified domain.

        - source_url - the url of the source
        - domain - the domain
        - config - an object with the attributes
            - http_port
            - domain
        """
        super().__init__(source, config)
        self._domain = domain


    @property
    def sub_domain(self):
        """The subdomain part of the proxy domain."""
        if self.domain.endswith(self._config.domain):
            return self.domain[:-len(self._config.domain) - 1]
        return None

    @property
    def domain(self):
        """The domain name to serve the content."""
        return self._domain
