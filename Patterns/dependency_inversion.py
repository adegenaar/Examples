"""
    Example of dependency inversion
"""

from abc import ABC, abstractmethod


class Switchable(ABC):
    """
    Switchable Base class for a switcable device interface

    Args:
        ABC (_type_): Abstract Base Class
    """

    def __init__(self) -> None:
        self.on = False

    def is_on(self) -> bool:
        """
        is_on is the device currently switched on

        Returns:
            bool:
        """
        return self.on

    @abstractmethod
    def turn_on(self) -> None:
        """
        turn_on change the state of the switch to on
        """
        self.on = True

    @abstractmethod
    def turn_off(self) -> None:
        """
        turn_off change the state of the switch to off
        """
        self.on = False


class LightBulb(Switchable):
    """
    LightBulb a subclass of Switchable

    Args:
        Switchable (_type_): base class
    """

    def turn_on(self) -> None:
        super().turn_on()
        print("LightBulb: turned on...")

    def turn_off(self) -> None:
        super().turn_off()
        print("LightBulb: turned off...")


class Fan(Switchable):
    """
    Fan

    Args:
        Switchable (_type_): base class
    """

    def turn_on(self) -> None:
        """
        turn_on inherited method
        """
        super().turn_on()
        print("Fan: turned on...")

    def turn_off(self) -> None:
        super().turn_off()
        print("Fan: turned off...")


class Switch:
    """
    Switch class
    """

    def __init__(self, switch: Switchable) -> None:
        self.client = switch

    def press(self) -> None:
        """
        press toggle the switch
        """
        if self.client.is_on():
            self.client.turn_off()
        else:
            self.client.turn_on()


light_switch = Switch(LightBulb())
light_switch.press()
light_switch.press()

fan_switch = Switch(Fan())
fan_switch.press()
fan_switch.press()
