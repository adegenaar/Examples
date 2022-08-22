"""
Examples of a Publisher/Subscriber interface using 
Monkey patching to extend the other classes
"""

# import functools
import inspect
from typing import Any

# todo: update for v3.10


def publisher():
    """
    publisher Python Decorator for the Observer Pattern
    """

    def subscribe(other, subscriber) -> None:
        """
        subscribe Adds the subscriber to the list of subscribers in the "other" object

        Args:
            other (object): The object that is going to be observed.
            observer (object): The subscriber object that will be receiving
                the updates from the observed object
        """
        if subscriber not in other._subscribers:
            other._subscribers.append(subscriber)

    def unsubscribe(other, subscriber) -> None:
        """
        unsubscribe Remove an object from the list of subscribers to be notified in the

        Args:
            other (object): The object that publishs changes to the subscriber list.
            subscriber (object): The object that reacts to the published changes
        """
        if subscriber is None:
            other._subscribers.removeAll()

        if subscriber in other._subscribers:
            other._subscribers.remove(subscriber)

    def publish(other, *args, **kwargs):
        """
        publish Notify the list of advertisers that an event has occurred

        Args:
            other (object): Object that is publishing the event to the list of subscribers
        """
        for subscriber in other._subscribers:
            # print("Inspect the subscriber:")
            # print("\tisclass(subscriber): ", inspect.isclass(subscriber))
            # print("\tismethod(subscriber): ", inspect.ismethod(subscriber))
            # print("\tisfunction(subscriber): ", inspect.isfunction(subscriber))
            # print("\tisinstance(subscriber): ", isinstance(subscriber, object))
            if inspect.ismethod(subscriber):
                subscriber(other, *args, **kwargs)
            elif inspect.isclass(subscriber):
                subscriber.update(other, *args, **kwargs)
            elif inspect.isfunction(subscriber):
                subscriber(other, *args, **kwargs)
            elif isinstance(subscriber, object):
                subscriber.update(other, *args, **kwargs)
            else:
                subscriber(*args, **kwargs)

    class ClassWrapper:
        """
        Inner wrapper object for the Python decoration of an object to take place
        """

        def __init__(self, cls):
            """
            __init__ Initialize the decoration of the class
            """
            self.other_class = cls

        def __call__(self, *cls_ars) -> Any:
            """
            __call__ used to create an instance of the class that is being decorated
                and connects the necessary methods for the class be a Publish/Subscriber

            Returns:
                object: Returns an instance of the encapsulated class after the Publish/Subscribe
                methods have been Monkey-Patched
            """
            other = self.other_class(*cls_ars)
            other._subscribers = []
            other.subscribe = subscribe.__get__(other)
            other.unsubscribe = unsubscribe.__get__(other)
            other.publish = publish.__get__(other)
            return other

    return ClassWrapper


@publisher()
class NormalClass:
    """
    Example class to demonstrate the use of the decorator
    """

    def __init__(self, name: str):
        """
        __init__ Initialize the object and store the name given to the instance.

        Args:
            name (str): name for this instance of the class
        """
        # self.name = name

    # def __repr__(self):
    #     """
    #     __repr__ format the name given

    #     Returns:
    #         str: name of the object instance
    #     """
    #     return str(self.name)

    def do_stuff(self):
        """
        do_stuff stand-in for the class method that needs to publish an event to all of the subscribers
        """
        # print ("publishing from " + self.name )
        self.publish()


class Subscriber:
    """
    Example class that responds to event notification from the example publisher
    """

    def __init__(self, name: str):
        """
        __init__ store the name of the instance of the

        Args:
            name (str): Name of the instance
        """
        # self.name = name

    # def __repr__(self):
    #     """
    #     __repr__ format the string name of the object instance of the

    #     Returns:
    #         str: name of the instance
    #     """
    #     return "Subscriber " + self.name

    def update(self, publisher, *args, **kwargs):
        """
        update Function called by the publisher when it is notifying the subscriber of an event to

        Args:
            publisher (object): object that published the event
        """
        # print (self.name + " was notified that " + publisher.name + " was updated!")
        print("Update notification!")
        # print (self)
        # print (publisher)

    def update2(self, publisher, *args, **kwargs):
        """
        update Function called by the publisher when it is notifying the subscriber of an event to

        Args:
            publisher (object): object that published the event
        """
        # print (self.name + " was notified that " + publisher.name + " was updated!")
        print("Update 2")
        # print(self)
        # print(publisher)


def func_update(publisher, *args, **kwargs):
    """
    update Function called by the publisher when it is notifying the subscriber of an event to

    Args:
        publisher (object): object that published the event
    """
    print("func_update notification!")


if __name__ == "__main__":
    print(Subscriber)
    print("__doc__: ", Subscriber.__doc__)
    print("__name__: ", Subscriber.__name__)

    A = NormalClass("A")
    B = NormalClass("B")

    o1 = Subscriber("1")
    o2 = Subscriber("2")

    A.subscribe(o1.update2)
    A.subscribe(o2)
    B.subscribe(func_update)

    A.do_stuff()
    B.do_stuff()
