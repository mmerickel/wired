"""
Simplest case: auto-generate a closure as the factory function.
"""

from wired import ServiceRegistry, wired_factory


@wired_factory
class LoginService:
    def __init__(self):
        ...


registry = ServiceRegistry()
