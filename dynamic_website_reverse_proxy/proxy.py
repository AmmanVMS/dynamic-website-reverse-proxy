"""
This module is the interface to the http proxy.

"""
import os


class Proxy:
    """Create a proxy class for a given domain name"""

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

    def __init__(self, config):
        """Create a new Proxy.
        
        - domain is the domain name of the service. New entries will be sub-entries of this.
        """
        self._websites = {} # id -> website
        self._config = config

    @property
    def domain(self):
        """The base domain for the dynamically configured websites."""
        return self._config.domain

    def add(self, website):
        """Add a website to the set of websites to serve."""
        self._websites[website.id] = website
        return website
    
    def get_nginx_configuration(self):
        """Get the nginx configuration."""
        websites = [website.get_nginx_configuration() for website in self.websites]
        return self.NGINX_CONFIGURATION.format(websites="\n".join(websites))
    
    @property
    def websites(self):
        """Read-only access to the websites of the proxy."""
        websites = self._websites.copy()
        for website in self._config.websites:
            websites[website.id] = website
        return list(websites.values())

    def reload(self, config):
        """Change the configuration of the proxy."""
        self._config = config
            

__all__ = ["Proxy"]

