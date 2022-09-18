"""
Test the websites served by default and configured though environment variables.

- default website configuration
- loading of websites from a parsed configuration
"""
import pytest
import os
from dynamic_website_reverse_proxy.tests.config import Config
from dynamic_website_reverse_proxy.proxy import DefaultWebsite

@pytest.mark.parametrize("url", [
    "https://example.com",
    "http://localhost:9001",
])
def test_default_website_loads_from_config(url):
    """The default_server attribute is important."""
    config = Config(default_server=url)
    website = DefaultWebsite(config)
    assert website.domain == "default_server"
    assert website.source_url == url


