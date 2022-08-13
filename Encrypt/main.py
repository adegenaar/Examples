"""main"""
from pathlib import Path
import key_generators
import key_storage
from key_factories import KeyGeneratorFactory, KeyStorageFactory


# def do_encrypt(fac: KeyGeneratorFactory) -> None:
#     """Do a test using a key generator and storage option."""

#     # retrieve the functions
#     key_generator = fac.get_key_generator()
#     key_storage = fac.get_key_storage()

#     # prepare the keys
#     key = key_storage.key
#     if not key:
#         key = key_generator.generate()
#         key_storage.key = key

#     # do the export
#     #folder = Path("/usr/tmp/video")
#     #video_exporter.do_export(folder)
#     #audio_exporter.do_export(folder)


def main() -> None:
    """ test """
    g = KeyGeneratorFactory()
    fkg = g.get_key_generator("FernetKeyGenerator")()
    key1 = fkg.generate()
    print (key1)

    s = KeyStorageFactory()
    fsg = s.get_key_storage("KeyFileStorage")(Path("key1.key"))
    fsg.key = key1


if __name__ == "__main__":
    main()
