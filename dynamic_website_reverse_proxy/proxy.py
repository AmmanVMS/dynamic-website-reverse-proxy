"""
This module is the interface to the http proxy.

"""
import os

APP_PORT = int(os.environ.get(("PORT", 9001))
NGINX_PORT = int(os.environ.get(("NGINX_PORT", 80))

NGINX_CONFIGURATION = """
#
# copied from https://gist.githubusercontent.com/nishantmodak/d08aae033775cb1a0f8a/raw/ebea0ae66e0a0188009accae2acba88cc646ddcd/nginx.conf.default
#

worker_processes  2;
#error_log /dev/stdout debug;

events {{
    worker_connections  1024;
}}

http {{
    default_type  application/octet-stream;
    log_format  main  '$remote_addr -> $http_host $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    sendfile        on;
    keepalive_timeout  65;
    gzip  on;
    #access_log off;
    access_log /dev/stdout;
    
    {websites}
}}
"""

class Website:
    """This is a website entered by the proxy."""
    
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
            http_port = self._config.http_port
            source_url = self.source_url
        )
    
    def is_served(self):
        """Whether the proxy serves this website."""
        return self.proxy.is_serving(self)
        
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


class DefaultWebsite(Website):
    """The website served by default."""

    def __init__(self, config):
        super().__init__()

    @property
    def domain(self):
        """Replaces the domain with the nginx wildcard for all other domains."""
        return "default_server"


class Proxy:
    """Create a proxy class for a given domain name"""

    def __init__(self, domain):
        """Create a new Proxy.
        
        - domain is the domain name of the service. New entries will be sub-entries of this.
        """
        self._domain = domain
        self._websites = {} # domain -> website
        self._local_website = LocalWebsite(self)

    @property
    def domain(self):
        """The base domain for the dynamically configured websites."""
        return self._domain

    def serve(self, scheme, host, port, subdomain):
        """Serve the content from the server address at the sub_domain.
        
        - scheme - http or https
        - host - the hostname
        - port - the port of the host
        - sub_domain - a valid domain name for a subdomain
        """
        source = urllib.parse.urlunsplit((scheme, host + ":" + port, "/", "", ""))
        website = Website(source, subdomain, self)
        self._websites[website.id] = website
        return website
    
    def get_nginx_configuration(self):
        """Get the nginx configuration."""
        websites = [website.get_nginx_configuration() for website in self.websites]
        websites.insert(0, self._local_website.get_nginx_configuration())
        return NGINX_CONFIGURATION.format(websites="".join(websites))
    
    def is_serving(self, website):
        """Whether the proxy is serving a website under this address."""
        return website == self._websites.get(website.domain)
    
    @property
    def websites(self):
        """Read-only access to the websites of the proxy."""
        return list(self._websites.values())
            

__all__ = ["Proxy", "APP_PORT"]

