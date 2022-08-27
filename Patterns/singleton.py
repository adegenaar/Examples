"""
    Classic Singleton class implementation
"""


class SingletonClass:
    """
    Classic Singleton class implementation
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance
