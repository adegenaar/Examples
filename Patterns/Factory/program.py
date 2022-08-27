"""
    Object Factory  Example Music Service
"""

import services

config = {
    "spotify_client_key": "THE_SPOTIFY_CLIENT_KEY",
    "spotify_client_secret": "THE_SPOTIFY_CLIENT_SECRET",
    "pandora_client_key": "THE_PANDORA_CLIENT_KEY",
    "pandora_client_secret": "THE_PANDORA_CLIENT_SECRET",
    "local_music_location": "/usr/data/music",
}


pandora = services.services.create("PANDORA", **config)
pandora.test_connection()

spotify = services.services.create("SPOTIFY", **config)
spotify.test_connection()

local = services.services.create("LOCAL", **config)
local.test_connection()

pandora2 = services.services.get("PANDORA", **config)
print(f"id(pandora) == id(pandora2): {id(pandora) == id(pandora2)}")

spotify2 = services.services.get("SPOTIFY", **config)
print(f"id(spotify) == id(spotify2): {id(spotify) == id(spotify2)}")
