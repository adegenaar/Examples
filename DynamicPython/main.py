""" Example of creating dynamic properties """
import json

# Unique type class to decipher between attributes
class ORMType:
    """basic types for the properties"""

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return str(self.value)


class BasicORM:
    """Basic ORM class"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, ORMType(key, value))

    def to_json(self):
        """Helper method to dump ORM instance to json"""
        obj = {}
        for attr in dir(self):
            if isinstance(getattr(self, attr), ORMType):
                obj[attr] = getattr(self, attr).value
        return json.dumps(obj)

    def from_json(self, json):
        """
        Helper method to convert a json object to a python object

        Args:
            json (JSON): JSON object to convert to a python object.
        """
        # loop over all of the json attributes and convert them to Python attributes
        for key, value in json.items():
            setattr(self, key, ORMType(key, value))


# Basic instance of ORM
textMessage = BasicORM(
    date="12/31/2020", uid="1234", user="nschairer", message="Simple text message"
)

###Display Text Message Information
print(textMessage.date)
print(textMessage.uid)
j = json.loads(textMessage.to_json())
print(j)

test = BasicORM()

test.from_json(j)
print(test.date)
print(test.uid)
