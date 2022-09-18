"""A website to serve."""


class Website:
    """This is a website registered in the proxy."""
    
    configuration_template = """
    server {{
        server_name {domain};
        listen 0.0.0.0:{http_port};
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

    def __init__(self, source_url, sub_domain, config):
        """Create a new website.

        - source_url - the url of the source
        - sub_domain - the first part of the domain
        - config - an object with the attributes
            - http_port
            - domain
        """
        self._source_url = source_url
        self._sub_domain = sub_domain
        self._config = config

    @property
    def sub_domain(self):
        """The subdomain part of the proxy domain."""
        return self._sub_domain

    @property
    def domain(self):
        """The domain name to serve the content."""
        return self.sub_domain + "." + self._config.domain

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
        return isinstance(other, Website) and self.id == other.id and self.source_url == other.source_url
    
    def __hash__(self):
        """Return the hash value."""
        return hash(self.id)
    
    def __repr__(self):
        """Return a text representation."""
        return "<Website {}>".format(self.id)

    @property
    def id(self):
        """Attribute to identify this website."""
        return self.domain
