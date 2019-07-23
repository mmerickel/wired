==============
Injected Field
==============

Our DI system now lets us use dataclasses to give the system instructions on how to create our dataclass instances.
Sometimes we want to give more instruction.
Let's see how to use the ``injected`` field to do so.

In the previous example, we had to pass in the customer to the ``__call__``.
Can't we get that from injection?
After all, we made a ``Customer`` and a ``FrenchCustomer`` and added it to the ``container`` in ``request.py``.

First, we'll make a small change in ``request.py`` to pass in a customer name during construction, rather than have a dataclass field default value:

.. literalinclude:: request.py
    :emphasize-lines: 14, 21

The ``Customer`` and ``FrenchCustomer`` dataclasses change slightly in ``models.py``, to not have a field default.
The bigger changes are in ``Greeter`` and ``FrenchGreeter``:

.. literalinclude:: models.py
    :emphasize-lines: 17, 23, 26, 31, 34-36, 44, 47-49

Foremost, we gain a new field that asks for a ``customer`` of the correct type (``Customer`` or ``FrenchCustomer``.)
We use the ``injected`` field helper to tell the injection system to get the value from the ``Context`` in the container.
As such, our ``factory`` decorator needs to ask for a ``context``.

With that, ``__call__`` no longer needs to have a ``customer`` name passed into it.
We have the correct ``customer`` on the dataclass instance, thanks to injection.

.. note::

    We could even eliminate ``__call__`` by using the dataclasses support for
    ``__post_init__`` to stash a customer name on the instance during construction.

What's happening behind the scenes?
``injected`` is a subclass of ``dataclasses.field`` which packs some information into the field metadata.
This metadata lets us give more instructions to the DI system.

Everything else in our app is the same, which shows our dataclasses can use DI to drive what they receive.
