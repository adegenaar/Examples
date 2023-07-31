"""
    Events
    ~~~~~~

    Implements C#-Style Events.

    Derived from the original work by Zoran Isailovski:
    http://code.activestate.com/recipes/410686/ - Copyright (c) 2005

    :copyright: (c) 2014-2017 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.

    Further enhancements by Albert Degenaar
"""

from collections.abc import Iterable
from typing import Any, Generator, Self


class _EventSlot:
    def __init__(self, name: str) -> None:
        self.targets = []
        self.__name__: str = name

    def __repr__(self) -> str:
        return f"event '{self.__name__}'"

    def __call__(self, *args, **kwargs) -> None:
        print(f"call({args=}, {kwargs=})")
        for fire in tuple(self.targets):
            fire(*args, **kwargs)

    def __iadd__(self, listener) -> Self:
        self.targets.append(listener)
        return self

    def __isub__(self, listener) -> Self:
        while listener in self.targets:
            self.targets.remove(listener)
        return self

    def __len__(self) -> int:
        return len(self.targets)

    def __iter__(self):
        def gen():
            for target in self.targets:
                yield target

        return gen()

    def __getitem__(self, key):
        return self.targets[key]


class Events:
    """
    Encapsulates the core to event subscription and event firing, and feels
    like a "natural" part of the language.

    The class Events is there mainly for 3 reasons:

        - Events (Slots) are added automatically, so there is no need to
        declare/create them separately. This is great for prototyping. (Note
        that `__events__` is optional and should primarilly help detect
        misspelled event names.)
        - To provide (and encapsulate) some level of introspection.
        - To "steel the name" and hereby remove unneeded redundancy in a call
        like:

            xxx.OnChange = event('OnChange')
    """

    def __init__(self, events: Iterable | None = None, event_slot_cls=_EventSlot):
        self.__event_slot_cls__ = event_slot_cls

        if events:
            if not isinstance(events, Iterable):
                raise AttributeError(f"type object {type(events)} is not iterable")
            self.__events__ = events

    def __getattr__(self, name) -> _EventSlot:
        if name.startswith("__"):
            raise AttributeError(
                f"type object '{self.__class__.__name__}' has no attribute '{name}'"
            )

        if hasattr(self, "__events__"):
            if name not in self.__events__:
                raise AttributeError("Event '{name}' is not declared")
        elif hasattr(self.__class__, "__events__"):
            if name not in self.__class__.__events__:  # type: ignore
                raise AttributeError("Event '{name}' is not declared")

        self.__dict__[name] = theevent = self.__event_slot_cls__(name)
        return theevent

    def __getitem__(self, item):
        return self.__dict__[item]

    def __repr__(self) -> str:
        return f"<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>"

    __str__ = __repr__

    def __len__(self) -> int:
        return len(list(self.__iter__()))

    def __iter__(self) -> Generator[_EventSlot, Any, None]:
        def gen(dictitems=self.__dict__.items()) -> Generator[_EventSlot, Any, None]:
            for _, val in dictitems:
                if isinstance(val, self.__event_slot_cls__):
                    yield val

        return gen()


if __name__ == "__main__":

    def on_change_callback(*args, **kwargs) -> None:
        """callback test"""
        print(f"on_change_callback({args=}, {kwargs=})")

    def on_delete_callback_args(*args, **kwargs) -> None:
        """callback test"""
        print(f"on_delete_callback_args({args=}, {kwargs=})")
        assert "arg1" in args
        assert 2 in args
        assert ("three", 3) in args
        assert "key" in kwargs

    MyEvents = Events(("on_change", "on_delete"))

    MyEvents.on_change += on_change_callback  # type: ignore # pylint: disable=E1101
    MyEvents.on_delete += on_delete_callback_args  # type: ignore # pylint: disable=E1101

    # fire the change event
    MyEvents.on_change()  # pylint: disable=E1101

    # fire the delete event
    MyEvents.on_delete("arg1", 2, ("three", 3), key="key")  # pylint: disable=E1101

    class MyEvents2(Events):
        """test class"""

        def __init__(self) -> None:
            super().__init__(("on_eventone",))
            # __events__: tuple[str] = ("on_eventOne",)
            # self.__slots__ = ("on_eventOne",)

    # MyEvents2.on_eventOne += on_change_callback

    myevent = MyEvents2()
    myevent.on_eventone += on_change_callback  # type: ignore # pylint: disable=E1101

    class CustomEventSlot(_EventSlot):
        """Custom event slot"""

    allevents: tuple[str, str] = ("on_change", "on_edit")

    class MyEvents3:
        """test class level events declarations"""

        events = Events(events=allevents, event_slot_cls=CustomEventSlot)
        events.on_change += on_change_callback  # type: ignore # pylint: disable=E1101
        events.on_change += on_change_callback  # type: ignore # pylint: disable=E1101
        events.on_edit += on_change_callback  # type: ignore # pylint: disable=E1101

    i = 0
    for event in MyEvents3.events:
        i += 1
        assert isinstance(event, CustomEventSlot)
    assert i == 2
