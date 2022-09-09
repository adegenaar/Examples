"""
Simple response hook
"""
import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def create_session() -> requests.Session:
    """
    _summary_
    """
    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json", "<token>": os.getenv("api_token")})

    def api_calls(response: requests.Response, *_args, **_kwargs):
        """
        how many calls are left?

        Args:
            response (response): response object
        """
        calls_left = response.headers["xxx-Api-Call-Limit"].split("/")
        print(calls_left)
        if calls_left[0] == calls_left[1] - 1:
            print("limit close, sleeping...")
            time.sleep(5)

    sess.hooks["response"] = api_calls

    return sess


def main():
    """
    main entry point
    """
    sess = create_session()
    resp = sess.get(os.getenv("api_url") + "/api/endpoint")
    print(resp)


if __name__ == "__main__":
    main()
