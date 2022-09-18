"""Base class for users."""

class UniqueUser:
    """A user on the system."""

    def __init__(self, name):
        """Create a unique user with this name"""
        self._name = name
    
    @property
    def name(self):
        """The name of the user."""
        return "🔒" + self._name

SYSTEM = UniqueUser("system")
