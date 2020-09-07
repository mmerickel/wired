"""
Simplest case: auto-generate a closure as the factory function.
"""

from wired import ServiceRegistry


class LoginService:
    def __init__(self):
        ...


registry = ServiceRegistry()
registry.register_service(LoginService)
