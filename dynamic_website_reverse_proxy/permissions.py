"""The permissions on this system."""
import os


class Permissions:
    """A set of permissions granted on this system."""

    def __init__(self, permissions):
        for permission in permissions:
            self.validate_and_raise(permission)
        self._permissions = set(permissions)

    def validate_and_raise(self, permission):
        """Validate a permission and raise an error if it is invalid."""
        if permission not in _ALL_PERMISSIONS_SET:
            raise InvalidPermissionError(f"'{permission}' must be one of these: \n" + "\n".join(ALL_PERMISSIONS))

    def allow(self, action):
        """Whether an action is allowed."""
        permission = action.as_permission()
        self.validate_and_raise(permission)
        return permission in self._permissions


ALL_PERMISSIONS = [
    f"{user} can {action} {obj} owned by {owner}"
    for user in "user admin system anonymous".split()
    for action in "see edit create delete".split()
    for obj in ("default website", "fqdn", "subdomain")
    for owner in ("user", "admin", "system", "anonymous", "other user")
    if not (user != "user" and owner == "user")
]

_ALL_PERMISSIONS_SET = set(ALL_PERMISSIONS)


class InvalidPermissionError(ValueError):
    """This error is raised when handling permissions that cannot be given."""


