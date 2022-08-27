"""
An example Local Service
"""
from pathlib import Path
from .music_service import MusicService


class LocalService:
    """
    An example of a Pandora service
    """

    def __init__(self, location):
        self._location = location

    def test_connection(self):
        """
        stub for testing the connection to Pandora
        """
        print(f"Accessing Local music at {self._location}")


def create_local_music_service(local_music_location: Path, **_ignored) -> MusicService:
    """
    Example implementation for a Spotify service builder
    """
    return LocalService(local_music_location)
