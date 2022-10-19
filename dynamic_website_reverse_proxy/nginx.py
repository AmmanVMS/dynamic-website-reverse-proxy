"""
This module controls the nginx server.
"""

import subprocess
import tempfile
import os


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
        return self._config.nginx_conf and subprocess.run(["which", "nginx"], stdout=None).returncode == 0


class NginxDatabaseObserver:
    """Observe the database and update nginx."""

    def __init__(self, config, db):
        """Create an instance."""
        self._db = db
        self._nginx = Nginx(config)
        db.attach(self)
        self.update()

    def update(self):
        """Restart nginx with a new configuration."""
        if self._nginx.is_available():
            self._nginx.configure(self._db.proxy.get_nginx_configuration())
