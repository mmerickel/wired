"""
Fail when provided an interface instead of class.
"""
from zope.interface import Interface

from wired import ServiceRegistry


class ILogin(Interface):
    ...


registry = ServiceRegistry()
registry.register_service(ILogin)
