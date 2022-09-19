"""Abilities that users have to act on this system."""

class Action:
    """Actions of users to be checked for permission."""

    def __init__(self, subject, predicate, object_):
        """Create a new action informed by the structure of the English language."""
        self._subject = subject
        self._predicate = predicate
        self._object = object_

    def as_permission(self):
        """Return a string that can be read as a permission."""
        return f"{self._subject.calls(self._subject)} can {self._predicate} {self._subject.calls(self._object)}"
    
    def as_denied_permission(self):
        """Return a string that can be read as a denied permission."""
        return f"{self._subject.calls(self._subject)} cannot {self._predicate} {self._subject.calls(self._object)}"
    

class Abilities:
    """The abilities a users have.

    This is also used as a spell checker for the permissions list.
    """

    def __init__(self, user):
        """Create a set of possible actions of a user."""
        self._user = user

    def see(self, something):
        """The user can see something."""
        return Action(self._user, "see", something)

    def edit(self, something):
        """The user can edit something."""
        return Action(self._user, "edit", something)

    def create(self, something):
        """The user can create something."""
        return Action(self._user, "create", something)

    def delete(self, something):
        """The user can delete something."""
        return Action(self._user, "delete", something)
