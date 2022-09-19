"""Test the permissions for the users."""
import pytest


class ANamedSomeone:
    """A mock class to be called something by a user."""

    def __init__(self, name):
        self.name = name

    def called_by(self, other):
        """How I would like the other to call me."""
        return self.name

    def is_unique_user(self):
        """Whether this is a unique user."""
        return False


class ANamer:
    """Someone who names a ANamesThing"""

    def call(self, other):
        return other.called_by(self)

@pytest.mark.parametrize("who", [
    ANamedSomeone("user"),
    ANamedSomeone("other user"),
    ANamedSomeone("system"),
])
def test_owned_website_has_a_name(who, website):
    website.change_owner_to(who)
    assert website.called_by(ANamer()) == f"website of {who.name}"
    