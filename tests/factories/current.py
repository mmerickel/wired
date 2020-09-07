"""
Mimic the pre-refactor behavior.
"""

from wired import ServiceRegistry


class LoginService:
    def __init__(self):
        ...


def login_factory(container):
    return LoginService()


registry = ServiceRegistry()
registry.register_factory(login_factory, LoginService)
