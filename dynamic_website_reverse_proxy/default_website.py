"""The Default website to display for unknown domain names.

"""
from .website import Website

DEFAULT_WEBSITE_ID = object()

class DefaultWebsite(Website):
    """The website served by default."""

    configuration_template = """
    server {{
        server_name {domain};
        # for default_server see https://linuxhint.com/what-is-default-server-in-nginx/
        listen {http_port} default_server;
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
        """Create a default website to serve when the domain is not used."""
        super().__init__(source_url, None, config)

    @property
    def sub_domain(self):
        """A default website has no subdomain."""
        raise ValueError("A default website has no subdomain.")

    @property
    def domain(self):
        """Replaces the domain with the nginx wildcard for all other domains."""
        return "_"

    @property
    def id(self):
        """The id of the default website. There is only one."""
        return DEFAULT_WEBSITE_ID

    def can_be_edited(self):
        """Whether the user can edit the website."""
        return False
