import pytest
import ReadTopic


def test_new_client():
    client = ReadTopic.connect_mqtt(True)
    assert client
