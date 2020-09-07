"""
Two decorators, one for a special case
"""

from wired import wired_factory


class Customer:
    pass


class CustomCustomer:
    pass


@wired_factory(context=Customer)
class LoginService:
    """ Generic for any context """

    def __init__(self):
        ...


@wired_factory(for_=LoginService, context=CustomCustomer)
class CustomLoginService:
    """ Override the default LoginService """

    def __init__(self):
        ...
