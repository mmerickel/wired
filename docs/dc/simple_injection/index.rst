================
Simple Injection
================

Finally, dependency injection (DI).

We want our greeting to have punctuation at the end, such as a period or, in the U.S., ``!!!`` because we Americans are like puppies.

Everything is the same as in :doc:`../decorators/index`, we just have different models:

.. literalinclude:: models.py
    :emphasize-lines: 7-11, 17, 21-22

- We register a dataclass ``Settings`` with one field, defaulted to a value of a period

- ``Greeter`` now asks DI to assign the configured ``Settings`` to a field...

- ...which is then used in the ``__call__``

So this is DI. What's actually happening?

``wired.dataclasses`` creates your dataclass instance. When it does, it looks at each field's type annotation. It uses this type to look in the registry for that configured type, then calls the factory to get an instance. Which it then stores on the field.

This is already useful and powerful. The "callee" and the "caller" have something in between -- DI -- which can help decouple calling. The callee -- the dataclass -- can provide instructions for what it wants provided -- hence the "inversion of control" expression. Here we are using ``dataclassses`` and its ``field`` construct as a DSL for object construction.

There's a lot more to this, as we'll see in the following sections.

To finish, we change our ``assert`` to add the period:

.. literalinclude:: ../../../tests/dataclasses/integration/test_dc_simple_injection.py
    :start-after: start-after
