"""
An example Spotify Service
"""
from .music_service import MusicService


class SpotifyService:
    """
    An example of a Spotify service
    """

    def __init__(self, access_code):
        self._access_code = access_code

    def test_connection(self):
        """
        stub for testing the connection to Spotify
        """
        print(f"Accessing Spotify with {self._access_code}")


class SpotifyServiceBuilder:
    """
    Example implementation for a Spotify service builder
    """

    def __init__(self):
        self._instance = None

    def __call__(
        self, spotify_client_key: str, spotify_client_secret: str, **_ignored
    ) -> MusicService:
        """
        An instance of the Spotify service is returned

        Args:
            spotify_client_key (_type_): _description_
            spotify_client_secret (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not self._instance:
            access_code = self.authorize(spotify_client_key, spotify_client_secret)
            self._instance = SpotifyService(access_code)
        return self._instance

    def authorize(self, _key: str, _secret: str) -> str:
        """
        Authorizes the Spotify service

        Args:
            key (str): the key into the config
            secret (str): example of a secret key to access the Spotify service

        Returns:
            str: _description_
        """
        return "SPOTIFY_ACCESS_CODE"
