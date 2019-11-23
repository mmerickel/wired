.. skip: start

=======================================
Overrides with ``for_`` and ``context``
=======================================

We have a ``Greeter`` that is used whenever our app asks for a ``Greeter``.
But maybe we want a second kind of ``Greeter``, used in a certain context.
For example, if we ask for a ``Greeter`` but the context is ``FrenchCustomer``, get a ``FrenchGreeter``.

Stated differently, we want:

- To register a ``FrenchGreeter``...

- To be used "for" ``Greeter``...

- ...when ``context is ``FrenchCustomer``

Our models are now richer. We add ``Customer``, ``FrenchCustomer``, and ``FrenchGreeter``:

.. literalinclude:: models.py
    :linenos:
    :emphasize-lines: 14-17, 20-23, 38-47

What's important here is this line:

.. code-block:: python

    @factory(for_=Greeter, context=FrenchCustomer)

This registers a dataclass to be used as the ``Greeter`` for the case when the ``context`` is a ``FrenchCustomer``.

Let's change our scenario to process two requests, meaning two customers.
In the first request the customer is a ``Customer``.
In the second, the customer is a ``FrenchCustomer``.
In both cases, we make a container for the request that sets the container's context to the customer instance.

.. literalinclude:: request.py
    :emphasize-lines: 16

To finish, we change our ``assert`` to test two cases:

.. literalinclude:: ../../../tests/dataclasses/integration/test_dc_overrides.py
    :start-after: start-after

With this, whenever the system asks for a ``Greeter``, if the container's current context is a ``FrenchCustomer``, they'll get ``FrenchGreeter`` instead of a plain ``Greeter``.
