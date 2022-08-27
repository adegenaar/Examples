"""
    PyTest module for testing the singleton
"""

from singleton import SingletonClass


def test_singleton():
    """
    test_singleton PyTest
    """
    singleton = SingletonClass()
    new_singleton = SingletonClass()

    assert singleton is new_singleton

    singleton.singl_variable = "Singleton Variable"
    assert new_singleton.singl_variable == singleton.singl_variable
