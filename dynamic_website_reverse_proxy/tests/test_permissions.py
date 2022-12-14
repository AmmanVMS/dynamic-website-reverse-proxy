"""Test the permissions for the users."""
import pytest
from dynamic_website_reverse_proxy.users import SYSTEM, ANONYMOUS, USER1, ADMIN, USER2
from dynamic_website_reverse_proxy.permissions import ALL_PERMISSIONS, Permissions, InvalidPermissionError
from dynamic_website_reverse_proxy.config import Config


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

    def calls(self, other):
        return other.called_by(self)

@pytest.mark.parametrize("who", [
    ANamedSomeone("user"),
    ANamedSomeone("other user"),
    ANamedSomeone("system"),
])
def test_owned_website_has_a_name(who, website):
    website.change_owner_to(who)
    assert website.called_by(ANamer()) == f"subdomain owned by {who.name}"


@pytest.mark.parametrize("action,string", [
    (SYSTEM.can.see(ANamedSomeone("lalala")), "system can see lalala"),
    (USER1.can.edit(ANamedSomeone("123")), "user can edit 123"),
    (ANONYMOUS.can.edit(ANamedSomeone("TEST!")), "anonymous can edit TEST!"),
    (ADMIN.can.create(ANamedSomeone("URGS")), "admin can create URGS"),
    (USER2.can.delete(ANamedSomeone("me")), "user can delete me"),
])
def test_action_as_string(action, string):
    assert action.as_permission() == string


class MockAction:

    def __init__(self, string):
        self.string = string

    def as_permission(self):
        return self.string

P2 = "admin can edit fqdn owned by system\nuser can see fqdn owned by admin"

@pytest.mark.parametrize("inside,permission,all_permissions", [
    # one permission
    (True, "user can see fqdn owned by user", "user can see fqdn owned by user"),
    (False, "system can see fqdn owned by other user", "user can see fqdn owned by user"),
    (False, "user can see fqdn owned by other user", "user can see fqdn owned by user"),
    (False, "system can see fqdn owned by other user", "user can see fqdn owned by system"),
    # multiple permissions
    (True, "admin can edit fqdn owned by system", P2),
    (True, "user can see fqdn owned by admin", P2),
    (False, "user can see fqdn owned by anonymous", P2),
    (False, "system can edit fqdn owned by other user", P2),
])
def test_can_load_permissions(inside, permission, all_permissions):
    p = Permissions(all_permissions.split("\n"))
    allowed = p.allow(MockAction(permission))
    assert allowed == inside, f"{permission} in {all_permissions} == {inside}"


invalid_permissions = pytest.mark.parametrize("invalid_permission", [
    # user cannot be in the end because the unique users identify themselves differently
    "admin can see fqdn owned by user",
    "anonymous can edit fqdn owned by user",
    "system can delete fqdn owned by user",
    # malformed permissions
    "user",
    "SYSTEM can see fqdn owned by system",
    " admin can see fqdn owned by system",
    "admin can see fqdn owned by system ",
])

@invalid_permissions
def test_load_invalid_permission(invalid_permission):
    with pytest.raises(InvalidPermissionError):
        Permissions(invalid_permission)


@invalid_permissions
def test_check_invalid_permission(invalid_permission):
    with pytest.raises(InvalidPermissionError):
        Permissions([]).allow(MockAction(invalid_permission))


def test_that_default_permissions_are_loaded():
    config = Config({})
    assert config.permissions.allow(MockAction("user can see fqdn owned by user"))
    assert not config.permissions.allow(MockAction("user can edit fqdn owned by system"))
