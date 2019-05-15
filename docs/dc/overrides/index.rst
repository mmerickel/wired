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

Now our request processing needs to handle two cases, the second of which we pass in a context which is a ``FrenchCustomer``:

.. literalinclude:: request.py
    :emphasize-lines: 16

To finish, we change our ``assert`` to test two cases:

.. literalinclude:: ../../../tests/dataclasses/integration/test_dc_overrides.py
    :start-after: start-after

With this, whenever the system asks for a ``Greeter``, if the current context is a ``FrenchCustomer``, they'll get ``FrenchGreeter`` instead of a plain ``Greeter``.
