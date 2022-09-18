import os
from bottle import run, route, static_file, redirect, post, request, re, SimpleTemplate, request
from .nginx import configure_nginx, nginx_is_available
from .CONFIG.database import CONFIG.database, NullCONFIG.database
import ipaddress
from .config import CONFIG
from .proxy_db import ProxyDB

# environment variables
HERE = os.path.dirname(__file__ or ".")

# constants
APPLICATION = __name__.split(".")[0]

# ValidIpAddressRegex and ValidHostnameRegex from https://stackoverflow.com/a/106223
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"


# The database to store the proxy in.
db = ProxyDB(CONFIG)
# make sure the proxy uses the updated environment variables
db.proxy.reconfigure()

def update_nginx():
    """Restart nginx with a new configuration."""
    if nginx_is_available():
        configure_nginx(proxy.get_nginx_configuration())
    else:
        print(db.proxy.get_nginx_configuration())
        print("NO NGINX")


@route("/")
def landing_page():
    """Redirect users from the landing page to the static files."""
    with open(os.path.join(HERE, "templates", "index.html")) as f:
        landing_page_template = SimpleTemplate(f.read())
    return landing_page_template.render(proxy=db.proxy, config=CONFIG)


@route("/static/<filename>")
def server_static(filename="index.html"):
    """Serve the static files."""
    return static_file(filename, root=CONFIG.static_files)


@post("/add-page")
def add_server_redirect():
    """Add a new page to redirect to."""
    # get parameters
    ip = request.forms.get("ip")
    port = request.forms.get("port")
    hostname = request.forms.get("name")
    scheme = "http"

    # validate parameters
    assert re.match(ValidHostnameRegex, hostname), "Hostname \"{}\" must match \"{}\"".format(hostname, ValidHostnameRegex)
    assert len(hostname) <= CONFIG.maximum_host_name_length, "The hostname \"{}\" must have maximum {} characters.".format(hostname, CONFIG.maximum_host_name_length)
    assert re.match(ValidIpAddressRegex, ip), "IP \"{}\" must match \"{}\"".format(ip, ValidIpAddressRegex)
    assert port.isdigit(), "A port must be a number, not \"{}\".".format(port)
    port = int(port)
    assert 0 < port < 65536, "The port must be in range, not \"{}\".".format(port)
    assert ipaddress.ip_address(ip) in CONFIG.network, "IP \"{}\" is expected to be in the CONFIG.network \"{}\"".format(ip, CONFIG.CONFIG.network)

    # add website
    source = urllib.parse.urlunsplit((scheme, host + ":" + str(port), "/", "", ""))
    website = Website(source, hostname, CONFIG)
    db.proxy.add(website)

    # save configuration
    db.save()
    update_nginx()
    redirect("/#" + website.id)


@route("/source.zip")
def get_source():
    """Download the source of this application."""
    # from http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python#6511788
    import tempfile, shutil, os
    directory = tempfile.mkdtemp()
    temp_path = os.path.join(directory, APPLICATION)
    zip_path = shutil.make_archive(temp_path, "zip", CONFIG.source_code)
    return static_file(APPLICATION + ".zip", root=directory)


def main():
    """Run the server app."""
    update_nginx()
    run(port=CONFIG.app_port, debug=CONFIG.debug, host="")

__all__ = ["main"]

