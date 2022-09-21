import os
from bottle import run, route, static_file, redirect, post, request, re, SimpleTemplate, request, Response
from .nginx import configure_nginx, nginx_is_available
import ipaddress
from .config import CONFIG
from .app_db import AppDB
from .website import Website
import urllib
from .users import ANONYMOUS, ADMIN
import json
from .api import APIv1 as APIv1Cls

# environment variables
HERE = os.path.dirname(__file__ or ".")

# constants
APPLICATION = __name__.split(".")[0]

# ValidIpAddressRegex and ValidHostnameRegex from https://stackoverflow.com/a/106223
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"


# The database to store the proxy in.
db = AppDB(CONFIG)
# make sure the proxy uses the updated environment variables
db.proxy.reload(CONFIG)

APIv1 = APIv1Cls(db, CONFIG)


def update_nginx():
    """Restart nginx with a new configuration."""
    if nginx_is_available():
        configure_nginx(db.proxy.get_nginx_configuration())
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
    source = urllib.parse.urlunsplit((scheme, ip + ":" + str(port), "/", "", ""))
    website = Website(source, hostname, CONFIG)
    db.proxy.add(website)

    # save configuration
    db.save()
    update_nginx()
    redirect("/#" + website.id)

def get_user_from_request():
    """Return the user who makes the request happen."""
    return ANONYMOUS

def make_response_from_api(result):
    """Return a bottle response from the API call."""
    body = json.dumps(result, indent="  ")
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        'Access-Control-Allow-Origin': '*',
        # see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowHeaderFromPreflight
        'Access-Control-Allow-Headers': request.headers.get("Access-Control-Request-Headers", ""),
        'Content-Type': 'application/json',
    }
    return Response(result["status"], body, headers)


@post("/api/v1/website/create")
def create_website(action, domain):
    return make_response_from_api(APIv1.create_website(request.auth, request.json()))


@get("/api/v1/website/list")
def list_websites():
    return make_response_from_api(APIv1.list_websites(request.auth))


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
    try:
        update_nginx()
    except:
        import traceback
        traceback.print_exc()
    run(port=CONFIG.app_port, debug=CONFIG.debug, host="")

__all__ = ["main"]

