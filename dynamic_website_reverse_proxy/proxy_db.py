"""Database for a proxy."""
from .proxy import Proxy


class ProxyDB:
    """A database wrapper so save and load proxies."""

    def __init__(self, config):
        """Create a new db with a configuration."""
        self.db = config.database
        self._proxy = self.db.load_safely()
        if self._proxy is None:
            self._proxy = Proxy.from_config(config)

    def save(self):
        """save the proxy"""
        self.db.save(self._proxy)

    @property
    def proxy(self):
        """Return the proxy."""
        return self._proxy
