"""
This module controls the nginx server.
"""

import subprocess
import tempfile
import os

# the value on which to ignore to configure nginx
DO_NOT_CONFIGURE_NGINX = "none"

class Nginx:
    """An object to handle the webserver."""

    def __init__(self, config):

        self._config = config
        self._current_process = None

    def configure(self, configuration):
        """Restart nginx with a certain configuration."""
        with open(self._config.nginx_conf, "w") as f:
            f.write(configuration)
        subprocess.run(["nginx", "-t", "-c", self._config.nginx_conf], check=True)
        if self._current_process:
            subprocess.run(["nginx", "-s", "reload"], check=True)
        else:
            self._current_process = subprocess.Popen(["nginx", "-c", self._config.nginx_conf])

    def is_available(self):
        """Return whether nginx is available."""
        return subprocess.run(["which", "nginx"], stdout=None).returncode == 0 and self._config.nginx_conf != DO_NOT_CONFIGURE_NGINX


__all__ = ["configure_nginx", "nginx_is_available"]

