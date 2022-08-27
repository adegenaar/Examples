"""
    Classic Singleton class implementation

    According to https://python-patterns.guide/gang-of-four/singleton/
    a better solution is to use a module level binding
    (see https://python-patterns.guide/python/module-globals/
    and https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules)
"""


class SingletonClass:
    """
    Classic Singleton class implementation
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance
