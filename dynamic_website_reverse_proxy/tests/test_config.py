"""Test the loading of the configuration"""

import os
import sys
from dynamic_website_reverse_proxy.config import Config, from_environment
import ipaddress
import pytest

HERE = os.path.dirname(__file__ or ".")
HERE_PARENT = os.path.dirname(HERE)

@pytest.mark.parametrize("attr,expected,env", [
    ("here", HERE_PARENT, {}),
    ("static_files", os.path.join(HERE_PARENT, "static"), {}),

    ("domain", "123.asd", {"DOMAIN": "123.asd"}),
    ("domain", "test.freifunk.net", {"DOMAIN": "test.freifunk.net"}),

    ("network", ipaddress.ip_network("10.22.0.0/16"), {"NETWORK": "10.22.0.0/16"}),
    ("network", ipaddress.ip_network("172.16.9.0/24"), {"NETWORK": "172.16.9.0/24"}),

    ("app_port", 9001, {}),
    ("app_port", 5000, {"PORT":"5000"}),

    ("http_port", 80, {}),
    ("http_port", 5000, {"HTTP_PORT":"5000"}),

    ("maximum_host_name_length", 50, {}),
    ("maximum_host_name_length", 5000, {"MAXIMUM_HOST_NAME_LENGTH":"5000"}),

    ("source_code", HERE_PARENT, {}),
    ("source_code", "/app", {"SOURCE_CODE":"/app"}),

    ("debug", True,  {}),
    ("debug", True,  {"DEBUG":""}),
    ("debug", True,  {"DEBUG":"true"}),
    ("debug", True,  {"DEBUG":"True"}),
    ("debug", True,  {"DEBUG":"TRUE"}),
    ("debug", False, {"DEBUG":"false"}),
    ("debug", False, {"DEBUG":"False"}),
    ("debug", False, {"DEBUG":"FALSE"}),

    ("default_server", "http://localhost:9001", {}),
    ("default_server", "http://localhost:4000", {"PORT": "4000"}),
    ("default_server", "http://test.example.com", {"DEFAULT_SERVER": "test.example.com"}),
    ("default_server", "https://test.example.com", {"DEFAULT_SERVER": "https://test.example.com"}),
])
def test_parsing(attr, expected, env):
    """Test the parsing of the configuration."""
    config = Config(env)
    config_value = getattr(config, value)
    assert config_value == expected

@pytest.mark.parametrize("is_persistent,env", [
    (True, {}),
    (False, {"DATABASE": "/tmp/db.pickle"}),
    (False, {"DATABASE": "/volume/db.pickle"}),
])
def test_database_type(is_persistent, env):
    """Which database to use."""
    config = Config(env)
    assert proxy.database.is_persistent() == is_persistent


@pytest.mark.parametrize("env", [
    {"DATABASE": "/tmp/db.pickle"},
    {"DATABASE": "/volume/db.pickle"},
])
def test_database_location(env):
    """Test where to store data."""
    config = Config(env)
    assert proxy.database.location == env["DATABASE"]


def test_pickled_env_config_is_identical():
    """Test that the environment configuration is identical when pickled.

    We need to make this sure so that nothing is ever saved.
    """
    conf = from_environment()
    loaded_conf = pickle.loads(pickle.dumps(conf))
    assert conf is loaded_conf


@pytest.mark.parametrize("expected,env_value,key,attr", [
    (True, "true", "DEBUG", "debug"),
    (False, "false", "DEBUG", "debug"),
])
def test_from_env_changes_when_env_changes(expected, env_value, key, attr):
    os.environ[key] = env_value
    conf = from_environment()
    value = getattr(conf, attr)
    assert value == expected    
    