"""Database for a proxy."""
from .proxy import Proxy


class ProxyDB:
    """A database wrapper so save and load proxies."""

    def __init__(self, config):
        """Create a new db with a configuration."""
        self._db = config.database
        self._proxy = self._db.load_safely()
        if self._proxy is None:
            self._proxy = Proxy(config)

    def save(self):
        """save the proxy"""
        self._db.save(self._proxy)

    @property
    def proxy(self):
        """Return the proxy."""
        return self._proxy
