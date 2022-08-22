"""
    Example of the Observer pattern
"""
import functools


class Observable:
    """
    Implements the functionality necessary for the notifying the Observer
    """

    def __init__(self):
        self._observers = []

    def register(self, observer):
        """
        register an observer for this object

        Args:
            observer (_type_): object that is observing this object
        """
        self._observers.append(observer)

    def notify(self, *arg, **kwargs):
        """
        notify the observer that something has happened
        """
        for observer in self._observers:
            if self != observer:
                observer.notify(self, *arg, **kwargs)


class Observer:
    """
    Implements the functionality necessary to be notified when something happens
    """

    def __init__(self, observable):
        self.register(observable)

    def notify(self, observable, *args, **kwargs):
        """
        notify callback

        Args:
            observable (_type_): object that sent the notification
        """
        print("Got", args, kwargs, " from ", observable)

    def register(self, observable):
        """
        register with a new observable object

        Args:
            observable (_type_): object that is being observed
        """
        observable.register(self)


if __name__ == "__main__":
    the_subject = Observable()
    the_observer = Observer(the_subject)
    the_subject.notify("test", kw="python")


# def register(types, func):
#     def wrapper_register(*args, **qwargs):
#         value = func(*args, **qwargs)
#         return value

#     _observers.append(func)
#     return wrapper_register


# def decorator(func):
#     @functools.wraps(func)
#     def wrapper_decorator(*args, **kwargs):
#         # Do something before
#         value = func(*args, **kwargs)
#         # Do something after
#         return value
#     return wrapper_decorator
