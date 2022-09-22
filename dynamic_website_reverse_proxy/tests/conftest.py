from pytest import fixture
import os
import sys
from .config import Config
from dynamic_website_reverse_proxy.website import Website
from dynamic_website_reverse_proxy.proxy import Proxy
from dynamic_website_reverse_proxy.database import Database
from unittest.mock import Mock
from dynamic_website_reverse_proxy.api import APIv1
from dynamic_website_reverse_proxy.app import App
from dynamic_website_reverse_proxy.users import SYSTEM, ADMIN, ANONYMOUS, USER1, USER2
import ipaddress
import json

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, "..", ".."))


@fixture(params=["proxy.freifunk.net", "in.net"])
def domain(request):
    """The domain name of the proxy"""
    return request.param

@fixture(params=[80, 8000])
def http_port(request):
    """The domain name of the proxy"""
    return request.param

@fixture
def config(domain, http_port):
    """The config to use."""
    return Config(domain=domain, http_port=http_port, websites=[])

@fixture
def proxy(config):
    """A Proxy to test."""
    return Proxy(config)


@fixture(params=["test", "sub.domain"])
def sub_domain(request):
    return request.param


@fixture(params=[
    "http://localhost:9090",
    "http://172.16.0.32",
    "https://other.domain"
])
def source(request):
    """A fictive but possible server address."""
    return request.param


@fixture
def website(source, sub_domain, config):
    """A website to serve."""
    return Website(source, sub_domain, config)


@fixture
def persistent_db(tmpdir):
    file = str(tmpdir.mkdir("sub").join("db.txt"))
    return Database(file)


@fixture
def db():
    """The database to operate the apiv1 on."""
    db = Mock()
    db.proxy.users = [USER1, USER2]
    return db

class TestPermissions:
    """Saving state."""
    def __init__(self):
        self.calls_left = 1
        self.actions = []

    def allow(self, action):
        self.actions.append(action.as_permission())
        self.calls_left -= 1
        return self.calls_left != 0

    def allow_all(self):
        """allow all calls"""
        self.calls_left = 0

@fixture
def permissions():
    """The permissions to grant."""
    return TestPermissions()

@fixture
def permission_granted(permissions):
    """Granting all permissions."""
    permissions.allow_all()
    return True

@fixture
def apiv1_config(permissions):
    config = {
        "maximum_host_name_length": 50,
        "network": ipaddress.ip_network("10.0.0.0/24"),
        "domain": "example.com",
        "admin_password": "secure",
        "websites": [],
    }
    return Config(permissions=permissions, **config)


class APIv1App:
    """Create an app around the API and see if it works."""
    def __init__(self, db, config):
        config.database = db
        self._app = App(config)
        self._app.request = self.request = Mock()
        self._app._apiv1._db.proxy.add = db.proxy.add

    def create_website(self, credentials, data):
        self.request.auth = credentials
        self.request.json.return_value = data
        response = self._app.create_website()
        response_data = json.loads(response.body)
        assert response_data["status"] == response.status_code
        return response_data

@fixture
def apiv1_app(db, apiv1_config):
    return APIv1App(db, apiv1_config)

@fixture
def apiv1_obj(db, apiv1_config):
    """The apiv1 object"""
    return APIv1(db, apiv1_config)

@fixture(params=[0, 1])
def apiv1(apiv1_obj, apiv1_app, request):
    return (apiv1_obj, apiv1_app)[request.param]

