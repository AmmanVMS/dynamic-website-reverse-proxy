"""Base class for users.

Users name other entities and can themselves be named.
Since this is a relationship, we use double dispatch.
"""
from .abilities import Abilities


class UniqueUser:
    """A user on the system."""

    def __init__(self, permission_name, id_, persistent_id):
        """Create a unique user with this name"""
        self._permission_name = permission_name
        self._id = id_
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

    @property
    def can(self):
        """What I can do."""
        return Abilities(self)

    @property
    def id(self):
        """The username/id in the system."""
        return self._id

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._permission_name}>"

SYSTEM = UniqueUser("system", "🔒system", "SYSTEM")
ADMIN = UniqueUser("admin", "admin", "ADMIN")
ANONYMOUS = UniqueUser("anonymous", "🔓anonymous", "ANONYMOUS")


class User:
    """A human user in the system. There can be many of that kind."""

    def __init__(self, name):
        """Create a new user with this name."""
        self._name = name

    @property
    def id(self):
        """The username/id in the system."""
        return self._name

    def calls(self, other):
        """How do I call this one? Hmm... Let's ask!"""
        return other.called_by(self)

    def called_by(self, other):
        """How I would like the other to call me."""
        if other.is_unique_user():
            return "other user"
        elif other.id == self.id:
            return "user"
        return "other user"

    def is_unique_user(self):
        """Whether this is a unique user."""
        return False

    @property
    def can(self):
        """What I can do."""
        return Abilities(self)



USER1 = User("Alice")
USER2 = User("Bob")








