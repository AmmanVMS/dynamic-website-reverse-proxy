import os
from bottle import static_file, redirect, request, SimpleTemplate, Response, default_app
from .nginx import Nginx
import ipaddress
from .config import CONFIG
from .app_db import AppDB
from .website import Website
import urllib
from .users import ANONYMOUS, ADMIN
import json
from .api import APIv1

# environment variables
HERE = os.path.dirname(__file__ or ".")

class App:
    """This is an app that uses bottle to serve web requests."""

    APPLICATION = __name__.split(".")[0]

    def __init__(self, config):
        """Create a new app with a configuration."""
        self.reload(config)
        self.request = request

    def reload(self, config):
        """Load the configuration again."""
        # The database to store the proxy in.
        db = AppDB(config)
        # make sure the proxy uses the updated environment variables
        db.proxy.reload(config)
        self._apiv1 = APIv1(db, config)
        self._nginx = Nginx(config)

    def update_nginx(self):
        """Restart nginx with a new configuration."""
        if self._nginx.is_available():
            self._nginx.configure(self._db.proxy.get_nginx_configuration())

    def make_response_from_api(self, result):
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
        return Response(body, result["status"], headers)

    REGISTER = {} # path -> method, name
    def serve_from(self, app):
        """serve from a bottle app"""
        for path, (method, name) in self.REGISTER.items():
            app.route(path, method, getattr(self, name))

    REGISTER["/api/v1/website/create"] = ("POST", "create_website")
    def create_website(self):
        return self.make_response_from_api(self._apiv1.create_website(self.request.auth, self.request.json()))


    REGISTER["/api/v1/website/list"] = ("GET", "list_websites")
    def list_websites(self):
        return self.make_response_from_api(self._apiv1.list_websites(self.request.auth))

    REGISTER["/source.zip"] = ("GET", "get_source")
    def get_source():
        """Download the source of this application."""
        # from http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python#6511788
        import tempfile, shutil, os
        directory = tempfile.mkdtemp()
        temp_path = os.path.join(directory, APPLICATION)
        zip_path = shutil.make_archive(temp_path, "zip", CONFIG.source_code)
        return static_file(APPLICATION + ".zip", root=directory)


class MainApp(App):
    """Improve this app for the main process."""

    def update_nginx(self):
        super().update_nginx()
        print(self._db.proxy.get_nginx_configuration())


def main(app=default_app()):
    """Run the server app."""
    api = MainApp(CONFIG)
    api.serve_from(app)
    app().run(port=CONFIG.app_port, debug=CONFIG.debug, host="")

__all__ = ["main"]

