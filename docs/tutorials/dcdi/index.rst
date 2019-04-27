.. skip: start

==================
Dataclasses and DI
==================

``wired`` says it can be the basis for a dependency injection (DI) framework.
What does that mean?

This tutorial shows you.
We build a custom DI system, bit by bit, resulting in a quite-capable application.
In fact, this tutorial served as the starting point for adding a dataclass-driven DI feature in ``wired``.

Which brings up a good point...we want ``wired`` to be not just a ready-to-go system.
We want it to have a small, minimal foundation that ideas can experiment atop.

.. note::

    We use the :doc:`final step of the tour <../tour/requests_views/index>` as the starting point for this tutorial.

Quick Taste
===========

What might this look like?
Imagine a ``View``, specific to ``FrenchCustomer``, that tells "the system" exactly what it wants:

.. code-block:: python

    @factory(for_=View, context=FrenchCustomer)
    @dataclass(frozen=True)
    class FrenchView:
        settings: Settings
        url: str = injected(Request, attr='url')
        customer_title: str = injected(Resource, attr='title')
        greeting: str = injected(Greeter, attr='greeting')

        def __call__(self) -> str:
            return f'{self.url} and FrenchView: {self.greeting} {self.customer_title} {self.settings.punctuation}'

Several interesting things here:

- We greatly decreased the surface area of what the view is expecting

- If you can construct this dataclass correctly, you have what you need to render

- In one case we ask for the entire "type" (``Settings``)

- ``Request`` and ``Resource`` point to instances quite unique to the currently-processing "request"

About This Tutorial
===================

We're using dataclasses, a new feature in Python 3.7 (but with a backport for Python 3.6.)
Dataclasses are unique in that they embrace Python type hinting.

One little known fact: they type information is actually available at runtime and dataclasses gives some helpers to introspect this.
The ``pydantic`` package, for example, does runtime *validation* of assigned data.

In this tutorial we put that annotation information to work. We make dataclasses our unit for *receiving* dependency injection, and we use those type annotations to communicate with the DI system we are building.
"Give me a Greeter", and the DI system will pass it into your dataclass.

But dataclasses have an extra idea: fields and field *metadata*.
We can use this as a way to communicate with the injector beyond "type". We can give instructions to the injector about what parts of an injectable we actually want, thus decreasing the "surface area" of injection.

Tutorial Steps
==============

.. toctree::
    :maxdepth: 1

    sniffing/index
    attributes/index
    decorators/index
