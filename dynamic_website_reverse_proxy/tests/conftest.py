from pytest import fixture
import os
import sys
from .config import Config

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, "..", ".."))


@fixture(params=["proxy.freifunk.net", "in.net"])
def domain(request):
    """The domain name of the proxy"""
    return request.param


@fixture
def config(domain):
    """The config to use."""
    return Config(domain=domain)

@fixture
def proxy(config):
    """A Proxy to test."""
    from dynamic_website_reverse_proxy.proxy import Proxy
    return Proxy(domain)


@fixture(params=["test", "sub.domain"])
def sub_domain(request):
    return request.param


@fixture(params=[("localhost", 9090), ("172.16.0.32", 80)])
def server_address(request):
    """A fictive but possible server address."""
    return request.param


@fixture
def website(server_address, sub_domain, proxy):
    """A website to serve."""
    from freifunk_website_proxy.proxy import Website
    return Website(server_address, sub_domain, proxy)


@fixture
def db(tmpdir):
    from freifunk_website_proxy.database import Database
    file = str(tmpdir.mkdir("sub").join("db.txt"))
    return Database(file)


