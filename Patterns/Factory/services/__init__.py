"""
Register the builders for all known services automatically
"""

from .music_service import MusicServiceProvider
from .spotify_service import SpotifyServiceBuilder
from .pandora_service import PandoraServiceBuilder
from .local_service import create_local_music_service

# Register the concrete builders with the factory
services = MusicServiceProvider()
services.register_builder("SPOTIFY", SpotifyServiceBuilder())
services.register_builder("PANDORA", PandoraServiceBuilder())
services.register_builder("LOCAL", create_local_music_service)
