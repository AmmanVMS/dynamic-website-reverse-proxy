from abc import ABC, abstractproperty
from .users import SYSTEM


class BaseWebsite(ABC):
    """This is a website registered in the proxy."""
    
    configuration_template = """
    server {{
        server_name {domain};
        listen {http_port};
        location / {{
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header User-Agent $http_user_agent;

#            client_max_body_size 100M;
            client_body_buffer_size 1m;
            proxy_intercept_errors on;
            proxy_buffering on;
            proxy_buffer_size 128k;
            proxy_buffers 256 16k;
            proxy_busy_buffers_size 256k;
            proxy_temp_file_write_size 256k;
            proxy_max_temp_file_size 0;
            proxy_read_timeout 300;

            proxy_pass {source_url};
        }}
    }}
    """

    def __init__(self, source_url, config):
        """Create a new website.

        - source_url - the url of the source
        - config - an object with the attributes
            - http_port
            - domain

        Until changed, the owner is the SYSTEM user.
        """
        self._source_url = source_url
        self._config = config
        self._owner = SYSTEM

    @abstractproperty
    def sub_domain(self):
        """The subdomain part of the proxy domain."""

    @abstractproperty
    def domain(self):
        """The domain name to serve the content."""

    @property
    def source_url(self):
        """The source url for the content so serve."""
        return self._source_url

    def get_nginx_configuration(self):
        """Return the nginx configuration for the website to serve"""
        return self.configuration_template.format(
            domain = self.domain,
            http_port = self._config.http_port,
            source_url = self.source_url,
        )
    
    def __eq__(self, other):
        """Return if the two websites are equal."""
        return isinstance(other, BaseWebsite) and self.id == other.id and self.source_url == other.source_url
    
    def __hash__(self):
        """Return the hash value."""
        return hash(self.id)
    
    def __repr__(self):
        """Return a text representation."""
        return f"<{self.__class__.__name__} {self.domain} -> {self.source_url}>"

    @property
    def id(self):
        """Attribute to identify this website."""
        if self.sub_domain is not None:
            return self.sub_domain
        return self.domain

    def can_be_edited(self):
        """Whether the user can edit the website."""
        return False

    def change_owner_to(self, new_owner):
        """Change the owner of the website."""
        self._owner = new_owner

    def called_by(self, user):
        """What this user calls me."""
        return f"website of {user.call(self._owner)}"

