Transitive Injection
====================

One thing can depend on another thing. For example, perhaps our Greeter greets a customer by name.
It ...needs the Customer, which might need the current Url from the container:

.. xxxcode-block:: python

    from .models import Context, Url, Settings

    @factory(for_=Context)
    @dataclass
    class Customer:
        url: str = injected(ServiceContainer, attr='url')
    @factory()
    @dataclass
    class Greeter:
        greeting: str = injected(Settings, attr='greeting')
        punctuation: str = injected(Settings, attr='punctuation')


