"""
Httpx example code.  for more details see https://python-httpx.org
"""

import httpx

# Now, let’s try to get a webpage.


r = httpx.get("https://httpbin.org/get")
print(r)
# <Response [200 OK]>
# Similarly, to make an HTTP POST request:


r = httpx.post("https://httpbin.org/post", data={"key": "value"})
# The PUT, DELETE, HEAD, and OPTIONS requests all follow the same style:
r = httpx.put("https://httpbin.org/put", data={"key": "value"})
r = httpx.delete("https://httpbin.org/delete")
r = httpx.head("https://httpbin.org/get")
r = httpx.options("https://httpbin.org/get")

# To include URL query parameters in the request, use the params keyword:


params = {"key1": "value1", "key2": "value2"}
r = httpx.get("https://httpbin.org/get", params=params)

print(r.url)
# URL('https://httpbin.org/get?key2=value2&key1=value1')

params = {"key1": "value1", "key2": ["value2", "value3"]}
r = httpx.get("https://httpbin.org/get", params=params)
print(r.url)
# URL('https://httpbin.org/get?key1=value1&key2=value2&key2=value3')

r = httpx.get("https://www.example.org/")
print(r.text)
#'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'

print(r.encoding)
#'UTF-8'

# For example, to create an image from binary data returned by a request, you can use the following code:
# >>> from PIL import Image
# >>> from io import BytesIO
# >>> i = Image.open(BytesIO(r.content))

url = "https://httpbin.org/headers"
headers = {"user-agent": "my-app/0.0.1"}
r = httpx.get(url, headers=headers)
