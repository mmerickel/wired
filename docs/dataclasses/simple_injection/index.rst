Default Field Values
====================

Maybe your dataclass asks for a type that isn't in the registry.
Dataclass default values to the rescue:

.. xxxcode-block:: python

    from dataclasses import dataclass
    from wired.dataclasses import factory

    @factory()
    @dataclass
    class Greeter:
        greeting: str = 'Hello'


Shows:

- Greeter.name from before

- Passing a value into the __call__, as before

- Greeter.punctuation, which is injected since...

- Punctuation is registered