"""
    Example implementation of a publish/subscribe mechanism
"""

# import functools
import inspect
from abc import ABC, abstractmethod


class Event(ABC):
    """
    Event to be published/subscribed

    Args:
        ABC (_type_): Abstract Base Class
    """

    def __init__(self):
        pass

    @abstractmethod
    def subscribe(self, subscriber, topic) -> None:
        """
        subscribe sign up to receive notifications

        Args:
            subscriber (_type_): Object that will receive notifications
        """

    @abstractmethod
    def publish(self, topic, *arg, **kwargs):
        """
        publish notifications to the _subscribers
        """


class UnnamedEvent(Event):
    """
    UnnamedEvent an event without a name

    Args:
        Event (_type_): SuperClass
    """

    def __init__(self):
        super().__init__()
        self._subscribers = []

    def subscribe(self, subscriber, topic):
        self._subscribers.append(subscriber)

    def publish(self, topic, *args, **kwargs):
        for subscriber in self._subscribers:
            if self != subscriber:
                if inspect.ismethod(subscriber):
                    subscriber(self, *args, **kwargs)
                else:
                    subscriber(*args, **kwargs)


class NamedEvent(Event):
    """
    NamedEvent is an Event with a name
    """

    def __init__(self):
        super().__init__()
        self._subscribers = {}

    def subscribe(self, subscriber, topic):
        # any other arguments are assumed to be topics
        if topic is None:
            raise ValueError("Named Events must have a topic")

        if not topic in self._subscribers:
            self._subscribers[topic] = []
        if not subscriber in self._subscribers[topic]:
            self._subscribers[topic].append(subscriber)

    def publish(self, topic, *args, **kwargs):
        if topic not in self._subscribers:
            return
        for observer in self._subscribers[topic]:
            if self == observer:
                return
            if inspect.ismethod(observer):
                observer(self, topic, *args, **kwargs)
            else:
                observer(topic, *args, **kwargs)


def notify_change(subscriber, *args, **kwargs):
    """
    notify_change tell all of the subscribers about the change

    Args:
        subscriber (_type_): _description_
    """
    print("Got a change: ", args, kwargs, " from ", subscriber)


class Observer:
    """
    object doing the observing
    """

    def __init__(self):
        pass

    def notify(self, subscriber, *args, **kwargs):
        """
        notification from the subscriber

        Args:
            subscriber (_type_): object being observed
        """
        print("Got notify:", self, args, kwargs, " from ", subscriber)

    def notify_unit_change(self, subscriber, *args, **kwargs):
        """
        notify_unit_change a unit has changed in the observed object

        Args:
            subscriber (_type_):  object being observed
        """
        print(f"Got unit change: {self} {args} {kwargs} from {subscriber}")

    @classmethod
    def notify_classmethod(cls, subscriber, *args, **kwargs):
        """
        notify_classmethod handle the notification with a class method

        Args:
            subscriber (_type_): object being observed
        """
        print("Got classmethod:", cls.__name__, args, kwargs, " from ", subscriber)


class Thermometer:
    """
    sample class to demonstrate the behavior of events
    """

    def __init__(self):
        self.event_manager = NamedEvent()

    def to_fahrenheit(self) -> float:
        """
        to_fahrenheit convert a value to fahrenheit

        Returns:
            _type_: _description_
        """
        value = self.temperature * 1.8 + 32
        self.event_manager.publish("fahrenheit", value)
        return value

    @property
    def temperature(self) -> float:
        """
        temperature return the current temperature

        Returns:
            float: the temperature
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        """
        temperature property setter

        Args:
            value (_type_): new value for the temperature

        Raises:
            ValueError: if the new value is too low, raise a ValueError
        """
        if value < -273.15:
            raise ValueError("The Temperature is below absolute zero!")
        self._temperature = value
        self.event_manager.publish("change", value)


if __name__ == "__main__":
    o1 = Observer()
    o2 = Observer()
    h1 = Thermometer()
    h2 = Thermometer()
    h1.event_manager.subscribe(notify_change, "change")  # no count
    h1.event_manager.subscribe(o2.notify, "fahrenheit")  # count
    h1.event_manager.subscribe(o1.notify, "change")  # count
    h1.event_manager.subscribe(o1.notify_classmethod, "change")  # no count
    h1.event_manager.subscribe(Observer.notify_classmethod, "fahrenheit")  # no count

    h1.temperature = 35
    h2.temperature = 100

    print(h2.to_fahrenheit())
