"""
Simple decorator usage
"""

from wired import wired_factory


@wired_factory()
class LoginService:
    def __init__(self):
        ...
