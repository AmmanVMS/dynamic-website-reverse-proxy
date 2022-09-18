

class Config:
    """Simple config class for the tests"""
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def new(self, **kw):
        d = self.__dict__.copy()
        d.update(kw)
        return self.__class__(**d)
