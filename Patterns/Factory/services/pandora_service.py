"""
An example Pandora service
"""

from typing import Any
from .music_service import MusicService


class PandoraService:
    """
    An example of a Pandora service
    """

    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret

    def test_connection(self):
        """
        stub for testing the connection to Pandora
        """
        print(f"Accessing Pandora with {self._key} and {self._secret}")


class PandoraServiceBuilder:
    """
    Example implementation for a Spotify service builder
    """

    def __init__(self):
        self._instance = None

    def __call__(self, pandora_client_key, pandora_client_secret, **_ignored) -> MusicService:
        if not self._instance:
            consumer_key, consumer_secret = self.authorize(
                pandora_client_key, pandora_client_secret
            )
            self._instance = PandoraService(consumer_key, consumer_secret)
        return self._instance

    def authorize(self, _key: str, _secret: str) -> Any:
        """
        Authorizes the Spotify service

        Args:
            key (str): the key into the config
            secret (str): example of a secret key to access the Pandora service

        Returns:
            str: a token to access the service
        """
        return ("PANDORA_CONSUMER_KEY", "PANDORA_CONSUMER_SECRET")
