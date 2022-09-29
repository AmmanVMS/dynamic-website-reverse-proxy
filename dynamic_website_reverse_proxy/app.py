import os
from bottle import static_file, redirect, request, Response, default_app, run, template, response
from .nginx import Nginx
import ipaddress
from .config import CONFIG
from .app_db import AppDB
from .website import Website
import urllib
from .users import ANONYMOUS, ADMIN
import json
from .api import APIv1
from http import HTTPStatus


# environment variables
HERE = os.path.dirname(__file__ or ".")

class App:
    """This is an app that uses bottle to serve web requests."""

    APPLICATION = __name__.split(".")[0]

    def __init__(self, config):
        """Create a new app with a configuration."""
        self.reload(config)
        self.request = request # for mocking in tests

    def reload(self, config):
        """Load the configuration again."""
        self._config = config
        # The database to store the proxy in.
        self._db = AppDB(config)
        # make sure the proxy uses the updated environment variables
        self._db.proxy.reload(config)
        self._apiv1 = APIv1(self._db, config)
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

    REGISTER["/"] = ("GET", "index")
    def index(self):
        credentials = self.get_cookie_credentials()
        logged_in, login_message, credentials = self._apiv1.get_login_response(credentials)
        websites = self._apiv1.list_websites(credentials)
        return template("index.html",
            template_lookup=self._config.template_lookup,
            websites=websites,
            config=self._config,
            login_message=login_message,
            logged_in=logged_in,
        )

    REGISTER["/static/<filename>"] = ("GET", "static_files")
    def static_files(self, filename):
        return static_file(filename, root=self._config.static_files)        

    REGISTER["/source.zip"] = ("GET", "get_source")
    def get_source():
        """Download the source of this application."""
        # from http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python#6511788
        import tempfile, shutil, os
        directory = tempfile.mkdtemp()
        temp_path = os.path.join(directory, self.APPLICATION)
        zip_path = shutil.make_archive(temp_path, "zip", self._config.source_code)
        return static_file(self.APPLICATION + ".zip", root=directory)

    REGISTER["/login"] = ("POST", "login")
    def login(self):
        """Log in a user."""
        response.set_cookie("username", request.forms.get('username'))
        response.set_cookie("password", request.forms.get('password'))
        return redirect("/", HTTPStatus.MOVED_PERMANENTLY)

    REGISTER["/logout"] = ("POST", "logout")
    def logout(self):
        """Log in a user."""
        response.delete_cookie("username")
        response.delete_cookie("password")
        return redirect("/", HTTPStatus.MOVED_PERMANENTLY)

    REGISTER["/save-website"] = ("POST", "save_website")
    def save_website(self):
        """Save a website that a user posted."""
        source = request.forms.get('source')
        if not source.startswith("http"):
            source = "http://" + source
        domain = request.forms.get('domain')
        if not "." in domain:
            domain += "." + self._config.domain
        website = {
            "domain": domain,
            "source": source
        }
        print(self._apiv1.create_website(self.get_cookie_credentials(), website))
        return redirect("/", HTTPStatus.MOVED_PERMANENTLY)

    def get_cookie_credentials(self):
        """Return the credentials for authentication."""
        username = request.get_cookie('username', None)
        if not username:
            return None # anonymous by default
        return username, request.get_cookie('password', "")

class MainApp(App):
    """Improve this app for the main process."""

    def update_nginx(self):
        super().update_nginx()
        print(self._db.proxy.get_nginx_configuration())


def main(appClass=MainApp, config=CONFIG):
    """Run the server app."""
    api = appClass(config)
    api.serve_from(default_app())
    api.update_nginx()
    run(port=config.app_port, debug=config.debug, host="")

__all__ = ["main"]

