"""
    simple test of the google translate
"""
#!/usr/bin/python
from google.cloud import translate_v2


def main():
    """
    main main entry point
    """

    translator = Translator()
    result = translator.translate("Mitä sinä teet")

    print(result.src)
    print(result.dest)
    print(result.origin)
    print(result.text)
    print(result.pronunciation)

    print(result.text)


if __name__ == "__main__":
    main()
