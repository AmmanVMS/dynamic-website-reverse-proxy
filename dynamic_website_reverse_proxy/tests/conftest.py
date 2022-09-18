from pytest import fixture
import os
import sys
from .config import Config
from dynamic_website_reverse_proxy.website import Website
from dynamic_website_reverse_proxy.proxy import Proxy
from dynamic_website_reverse_proxy.database import Database



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
    return Config(domain=domain, http_port=http_port)

@fixture
def proxy(config):
    """A Proxy to test."""
    return Proxy(domain)


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
def db(tmpdir):
    file = str(tmpdir.mkdir("sub").join("db.txt"))
    return Database(file)


