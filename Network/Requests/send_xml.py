""" Simple sending POST request example"""
import requests


def sendxml(url: str, xml: str):
    """send xml in a POST"""
    headers = {"Content-Type": "application/xml"}  # set what your server

    res = requests.post(url, data=xml.encode("utf-8"), headers=headers)
    print(res)
    print(res.json())


def sendfile(url: str, filename: str):
    """send a file"""
    with open(filename, "rb") as f:
        files = {"my_file": f}
        res = requests.post(url, files=files)
        print(res.text)
        print(res.json())


def main():
    """main"""
    # url = "http://127.0.0.1:8000/file"
    # sendfile(url, "readme.md")

    url = "http://127.0.0.1:8000/xml"
    xml = (
        """<?xml version='1.0' encoding='utf-8'?><Item><name>Fred</name><price>10</price></Item>"""
    )
    # xml = "</>"
    sendxml(url, xml)


if __name__ == "__main__":
    main()
