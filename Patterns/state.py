"""
Simple example for the State pattern
"""

from abc import ABC, abstractmethod
from typing import Any

class State(ABC):
    """
    Abstract Base Class for the states
    """
    @property
    def context(self) -> Any:
        """
        returns the current context object

        Returns:
            Context: controlling object
        """
        return self._context

    @context.setter
    def context(self, context: Any) -> None:
        self._context = context

    @abstractmethod
    def do_something(self) -> None:
        """
        Stand-in for the action a state would take
        """




class Context:
    """
    the context class contains a _state that references the concrete 
    state and set_state method to change between states.
    """

    _state = None

    def __init__(self, state: State) -> None:
        self.set_state(state)

    def set_state(self, state: State):
        """
        set the current state to the new states

        Args:
            state (State): new state to transistion to
        """
        print(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def do_something(self):
        """
        Stub for the action a real state implementation would have
        """
        self._state.do_something()


class ConcreteStateA(State):
    """
    A Concrete State that simply transitions to the next state

    Args:
        State (_type_): the next state
    """
    def do_something(self) -> None:
        print("The context is in the state of ConcreteStateA.")
        print("ConcreteStateA now changes the state of the context.")
        self.context.set_state(ConcreteStateB())


class ConcreteStateB(State):
    """
    A Concrete State that simply transitions to the next state

    Args:
        State (_type_): the next state
    """
    def do_something(self) -> None:
        print("The context is in the state of ConcreteStateB.")
        print("ConcreteStateB wants to change the state of the context.")
        self.context.set_state(ConcreteStateA())


if __name__ == "__main__":
    # sample application
    app = Context(ConcreteStateA())
    app.do_something()    # this method is executed as in state 1
    app.do_something()    # this method is executed as in state 2
