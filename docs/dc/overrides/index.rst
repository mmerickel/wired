
Overrides with ``for_`` and ``context``
=======================================

We have a ``Greeter`` that is used whenever our app asks for a ``Greeter``.
But maybe we want a second kind of ``Greeter``, used in a certain context.
For example, if we ask for a ``Greeter`` but the context is ``FrenchCustomer``, get a ``FrenchGreeter``.

Stated differently, we want:

- To register a ``FrenchGreeter``...

- To be used "for" ``Greeter``...

- ...when ``context is ``FrenchCustomer``

The imperative version would be this:

.. xxxcode-block:: python

    from .models import Greeter, FrenchCustomer

    @dataclass
    class FrenchGreeter:
        settings: Settings

    # Presumes an existing registry instance
    register_dataclass(registry, FrenchGreeter,
        for_=Greeter, context=FrenchCustomer)

The decorator version, in this case, shows that ``factory`` takes those arguments:

.. xxxcode-block:: python

    @factory(for_=Greeter, context=FrenchCustomer)
    @dataclass
    class FrenchGreeter:
        settings: Settings

With that, whenever someone asks for a ``Greeter``, if the current context is a ``FrenchCustomer``, they'll get ``FrenchGreeter`` instead.
