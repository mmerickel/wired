"""
Simple decorator usage but passing in context etc.
"""

from wired import ServiceRegistry, wired_factory


@wired_factory
class LoginService:
    def __init__(self):
        ...


registry = ServiceRegistry()
