"""Simple config class for the tests"""

class Config:
    """A test config."""
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def new(self, **kw):
        d = self.__dict__.copy()
        d.update(kw)
        return self.__class__(**d)
