"""Base class for users.

Users name other entities and can themselves be named.
Since this is a relationship, we use double dispatch.
"""
from .abilities import Abilities
import hashlib
import os


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

    DEFAULT_PASSWORD = ""

    def __init__(self, name):
        """Create a new user with this name."""
        self._name = name
        self._salt = os.urandom(10)
        self._algorithm = hashlib.sha1 # store in user in case of change
        self.set_password(self.DEFAULT_PASSWORD)

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

    def set_password(self, new_password):
        """Set a new password for the user."""
        self._password = self._algorithm(self._salt + new_password.encode("UTF-8")).digest()
    
    def is_password(self, password):
        """Return whether the password is the correct password of this user."""
        _password = self._algorithm(self._salt + password.encode("UTF-8")).digest()
        return _password == self._password


USER1 = User("Alice")
USER1.test_password = "1234"
USER1.set_password("1234")

USER2 = User("Bob")
USER2.test_password = "password"
USER2.set_password("password")

USER3 = User("Molly")
USER3.test_password = "nanna"
USER3.set_password("nanna")








