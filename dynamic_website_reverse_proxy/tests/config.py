"""An easily configurable class for configuration.

"""
import pytest


class Config:
    """Simple config class for the tests"""
    def __init__(self, **kw):
        """Create a new config with the given key words."""
        self.__dict__.update(kw)

    def new(self, **kw):
        """Return a new config with the given key words and this one."""
        d = self.__dict__.copy()
        d.update(kw)
        return self.__class__(**d)

    def update(self, **kw):
        """Update or add configuration from kw."""
        self.__dict__.update(kw)