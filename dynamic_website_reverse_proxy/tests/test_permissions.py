"""Test the permissions for the users."""
import pytest
from dynamic_website_reverse_proxy.users import SYSTEM, ANONYMOUS, USER1, ADMIN, USER2


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


@pytest.mark.parametrize("action,string", [
    (SYSTEM.can.see(ANamedSomeone("lalala")), "system can see lalala"),
    (USER1.can.edit(ANamedSomeone("123")), "user can edit 123"),
    (ANONYMOUS.can.edit(ANamedSomeone("TEST!")), "anonymous can edit TEST!"),
    (ADMIN.can.create(ANamedSomeone("URGS")), "admin can create URGS"),
    (USER2.can.delete(ANamedSomeone("me")), "user can delete me"),
])
def test_action_as_string(action, string):
    assert action.as_permission() == string



