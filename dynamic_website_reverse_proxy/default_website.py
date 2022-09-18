"""The Default website to display for unknown domain names.

"""

class DefaultWebsite(Website):
    """The website served by default."""

    @property
    def domain(self):
        """Replaces the domain with the nginx wildcard for all other domains."""
        return "default_server"
