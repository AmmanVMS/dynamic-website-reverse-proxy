"""
This module controls the nginx server.
"""

import subprocess
import tempfile
import os

NGINX_CONF = os.environ.get("NGINX_CONF", "/tmp/nginx.conf")
current_process = None

def configure_nginx(configuration):
    """Restart nginx with a certain configuration."""
    global current_process
    with open(NGINX_CONF, "w") as f:
        f.write(configuration)
    subprocess.run(["nginx", "-t", "-c", NGINX_CONF], check=True)
    if current_process:
        subprocess.run(["nginx", "-s", "reload"], check=True)
    else:
        current_process = subprocess.Popen(["nginx", "-c", NGINX_CONF])
    print(configuration)


def nginx_is_available():
    """Return whether nginx is available."""
    return subprocess.run(["which", "nginx"], stdout=None).returncode == 0


__all__ = ["configure_nginx", "nginx_is_available"]

