"""Base class for users.

Users name other entities and can themselves be named.
Since this is a relationship, we use double dispatch.
"""

class UniqueUser:
    """A user on the system."""

    def __init__(self, permission_name, display_name, persistent_id):
        """Create a unique user with this name"""
        self._permission_name = permission_name
        self._display_name = display_name
        self._persistent_id = persistent_id

    def __reduce__(self):
        """Make identity through pickle work."""
        return self._persistent_id

    def calls(self, other):
        """How do I call this one? Hmm... Let's ask!"""
        return other.called_by(self)
        
    def called_by(self, other):
        """How I would like the other to call me."""
        return self._permission_name

    def is_unique_user(self):
        """Whether this is a unique user."""
        return True

SYSTEM = UniqueUser("system", "🔒system", "SYSTEM")
ADMIN = UniqueUser("admin", "admin", "ADMIN")
ANONYMOUS = UniqueUser("anonymous", "🔓anonymous", "ANONYMOUS")


class User:
    """A human user in the system. There can be many of that kind."""

    def __init__(self, name):
        """Create a new user with this name."""
        self._name = name

    @property
    def name(self):
        """The username."""
        return self._name

    def calls(self, other):
        """How do I call this one? Hmm... Let's ask!"""
        return other.called_by(self)

    def called_by(self, other):
        """How I would like the other to call me."""
        if other.is_unique_user():
            return "other user"
        elif other.name == self.name:
            return "user"
        return "other user"

    def is_unique_user(self):
        """Whether this is a unique user."""
        return False


USER1 = User("Alice")
USER2 = User("Bob")







