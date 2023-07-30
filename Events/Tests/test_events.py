from typing import Literal

import pytest

from events import Events, _EventSlot


class TestBase:
    def callback1(self) -> None:
        pass

    def callback2(self) -> None:
        pass

    def callback3(self) -> None:
        pass


class TestEvents(TestBase):
    def test_getattr(self) -> None:
        class MyEvents(Events):
            def __init__(self) -> None:
                super().__init__(("on_eventOne",))

        with pytest.raises(AttributeError):
            MyEvents().on_eventNotOne += self.callback1

        MyEvents().on_eventOne += self.callback1

        myevent = MyEvents()
        with pytest.raises(AttributeError):
            myevent.on_eventNotOne += self.callback1
        myevent.on_eventOne += self.callback1

    def test_len(self):
        """We want __events__ to be set to verify that it is not counted as part of __len__."""

        class MyEvents:
            """test class"""

            def __init__(self) -> None:
                self.events = Events(events=("on_change", "on_get"))

        myevents = MyEvents()

        myevents.events.on_change += self.callback1
        myevents.events.on_get += self.callback2
        assert len(myevents.events) == 2

    def test_iter(self) -> None:
        class MyEvents:
            def __init__(self) -> None:
                self.events = Events()

        myevents = MyEvents()

        myevents.events.on_change += self.callback1
        myevents.events.on_change += self.callback2
        myevents.events.on_edit += self.callback1
        i = 0
        for event in myevents.events:
            i += 1
            assert isinstance(event, _EventSlot)
        assert i == 2

    def test_iter_custom_event_slot_cls(self) -> None:
        """test creating a custom event slot"""

        class CustomEventSlot(_EventSlot):
            """Custom event slot"""

        allevents: tuple[str, str] = ("on_change", "on_edit")

        class MyEvents(TestBase):
            def __init__(self) -> None:
                self.events = Events(events=allevents, event_slot_cls=CustomEventSlot)
                self.events.on_change += self.callback1
                self.events.on_change += self.callback2
                self.events.on_edit += self.callback1

        i = 0
        for event in MyEvents().events:
            i += 1
            assert isinstance(event, CustomEventSlot)
        assert i == 2

    def test_event_slot_cls_default(self):
        class MyEvents:
            def __init__(self) -> None:
                self.events = Events()

        myevents = MyEvents()
        assert _EventSlot == myevents.events.__event_slot_cls__

    def test_event_slot_cls_custom(self) -> None:
        class CustomEventSlot(_EventSlot):
            """Custom event slot"""

        class MyEvents:
            """Event test class"""

            def __init__(self, cls: type[_EventSlot]) -> None:
                self.events = Events(event_slot_cls=cls)

        custom = MyEvents(cls=CustomEventSlot)
        assert CustomEventSlot == custom.events.__event_slot_cls__


class TestEventSlot(TestBase):
    """
    Tests for the event slot
    """

    class MyEvents(TestBase):
        """Test class used for all of the tests"""

        def __init__(self) -> None:
            self.events = Events()
            self.events.on_change += self.callback1
            self.events.on_change += self.callback2
            self.events.on_change += self.callback3
            self.events.on_edit += self.callback3

    def test_type(self) -> None:
        """Type checking the event that should be fired"""
        myevents = self.MyEvents()

        ev: _EventSlot = myevents.events.on_change
        assert isinstance(ev, _EventSlot)
        assert ev.__name__ == "on_change"

    def test_len(self) -> None:
        myevents = self.MyEvents()
        assert len(myevents.events.on_change) == 3
        assert len(myevents.events.on_edit) == 1

    def test_repr(self) -> None:
        myevents = self.MyEvents()
        ev: _EventSlot = myevents.events.on_change
        assert ev.__repr__() == "event 'on_change'"

    def test_iter(self) -> None:
        myevents = self.MyEvents()
        ev: _EventSlot = myevents.events.on_change
        assert len(ev) == 3
        i = 0
        for target in ev:
            i += 1
            assert target.__name__ == f"callback{i}"

    def test_getitem(self) -> None:
        myevents = self.MyEvents()
        ev: _EventSlot = myevents.events.on_edit
        assert len(ev) == 1
        assert ev[0].__name__ == "callback3"

        with pytest.raises(IndexError):
            ev[1]

        # test the
        assert ev is myevents.events["on_edit"]
        assert ev is not myevents.events["on_change"]
        with pytest.raises(KeyError):
            myevents.events["on_nonexistent_event"]

    def test_isub(self) -> None:
        myevents = self.MyEvents()
        myevents.events.on_change -= myevents.callback1
        ev: _EventSlot = myevents.events.on_change
        assert len(ev) == 2
        assert ev[0].__name__ == "callback2"
        assert ev[1].__name__ == "callback3"


class TestInstanceEvents(TestBase):
    def test_getattr(self) -> None:
        MyEvents = Events(("on_eventOne",))

        MyEvents.on_eventOne += self.callback1

        with pytest.raises(AttributeError):
            MyEvents.on_eventNotOne += self.callback1

        with pytest.raises(AttributeError):
            MyEvents.events.on_eventNotOne += self.callback1

    def test_instance_restriction(self) -> None:
        class MyEvents(Events):
            """Test class"""

        # Create an event instance pre-populatd with specific events
        my_restricted_instance = MyEvents(("on_everytwo",))

        # should work
        my_restricted_instance.on_everytwo += self.callback1

        # should fail as on_everyone was not defined
        with pytest.raises(AttributeError):
            my_restricted_instance.on_everyone += self.callback1


def on_change_callback(*args, **kwargs) -> None:
    raise ValueError("on_change_callback")


def on_delete_callback_args(*args, **kwargs) -> None:
    assert "arg1" in args
    assert 2 in args
    assert ("three", 3) in args
    assert "key" in kwargs


class TestFunctionCallback:
    def on_change_callback(self, *args, **kwargs) -> None:
        raise ValueError("on_change_callback")

    def on_delete_callback_args(self, *args, **kwargs) -> None:
        assert "arg1" in args
        assert 2 in args
        assert ("three", 3) in args
        assert "key" in kwargs

    def callback3(self) -> None:
        pass

    def test_member_function_callback(self) -> None:
        MyEvents = Events(("on_change", "on_delete"))

        MyEvents.on_change += self.on_change_callback
        MyEvents.on_delete += self.on_delete_callback_args
        with pytest.raises(ValueError):
            MyEvents.on_change()

        MyEvents.on_delete("arg1", 2, ("three", 3), key="key")

    def test_function_callback(self) -> None:
        MyEvents = Events(("on_change", "on_delete"))

        # use the non-member functions for this test
        MyEvents.on_change += on_change_callback
        MyEvents.on_delete += on_delete_callback_args
        with pytest.raises(ValueError):
            MyEvents.on_change()

        MyEvents.on_delete("arg1", 2, ("three", 3), key="key")
