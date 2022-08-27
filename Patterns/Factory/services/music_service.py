"""
_summary_
"""
from typing import Protocol
from object_factory import ObjectFactory


class MusicService(Protocol):
    """
    A protocol defined for the MusicService
    """

    def test_connection(self):
        """
        All MusicServices must have a test_connection member
        """


class MusicServiceProvider(ObjectFactory):
    """
    Specialized version of the Object Factory
    """

    def get(self, service_id: str, **kwargs) -> MusicService:
        """
        Simplifies the creation for a MusicService

        Args:
            service_id (_type_): id of the service

        Returns:
            MusicService: An instance of a MusicService supporting class
        """
        return self.create(service_id, **kwargs)
