"""Database for a proxy."""
from .proxy import Proxy

ENTRY_PROXY = 'proxy'
ENTRY_VERSION = 'VERSION'

class AppDB:
    """A database wrapper so save and load proxies."""

    VERSION = 1

    def __init__(self, config):
        """Create a new db with a configuration."""
        self.observers = []
        self._db = config.database
        self._config = config
        self._data = self._db.load_safely()
        if type(self._data) is not dict or self._data.get(ENTRY_VERSION) != self.VERSION:
            self.initialize()

    def attach(self, observer):
        """Add an observer to this database."""
        self.observers.append(observer)

    def notifyAllObservers(self):
        """There was a change so we should tell everyone!"""
        for observer in self.observers:
            observer.update()

    def initialize(self):
        """Setup the database from scratch."""
        self._data = {
            ENTRY_VERSION: self.VERSION,
            ENTRY_PROXY: Proxy(self._config)
        }
        self.notifyAllObservers()

    def save(self):
        """save the proxy"""
        self._db.save(self._data)
        self.notifyAllObservers()

    @property
    def proxy(self):
        """Return the proxy."""
        return self._data[ENTRY_PROXY]
