"""
Generic Implementation of an Object Factory

Raises:
    ValueError: No builder defined for the given key
"""


class ObjectFactory:
    """
    Object Factory implementation

    Methods:
        register_builder (key, builder)
        create (key, **kwargs)
    """

    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        """
        Method to register a builder for the given key

        Args:
            key (str): key used to identify the builder function/method
            builder (callable): a Callable used to create an instance of an class
        """

        self._builders[key] = builder

    def create(self, key: str, **kwargs) -> object:
        """
        Create an instance of a class using the given key/builder

        Args:
            key (str): unique identifer for the builder

        Raises:
            ValueError: unable to locate a builder for the given key

        Returns:
            Object: an instance of the class created by the builder
        """
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
