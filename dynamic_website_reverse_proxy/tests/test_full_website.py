"""Tests for the full website.
"""

from .config import Config
from ..full_website import FullWebsite
import pytest


@pytest.mark.parametrize("domain,full,id", [
    ("test.a.b", "test.example.com", "test.example.com"),
    ("example.com", "a.example.com", "a"),
])
def test_that_the_id_is_relative_if_possible(domain, full, id):
    website = FullWebsite("http://localhost", full, Config(domain=domain))
    assert website.id == id


