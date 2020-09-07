"""
Imperatively register a function that type hints a return type
"""
from wired import ServiceContainer, wired_factory


@wired_factory()
class Customer:
    def __init__(self):
        self.name = 'Some Customer'


class LoginService:
    def __init__(self, customer_name):
        self.customer_name = customer_name


@wired_factory()
def make_login_service(container: ServiceContainer) -> LoginService:
    customer: Customer = container.get(Customer)
    return LoginService(customer_name=customer.name)
