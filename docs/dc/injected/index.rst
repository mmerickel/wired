==============
Injected Field
==============

Our DI system now lets us use dataclasses to give the system instructions on how to create our instances.
Sometimes we want to give more instruction.
Let's see how to use the ``injected`` field to do so.

What if you want a different type than the factory?
In the previous step, we asked for ``Context``.
But the type is really ``Customer``.
We'll solve that problem with ``injected``, a dataclass field constructor.

In ``models.py``, we simplify ``Greeter`` by assigning a ``customer`` instead of a ``context``:

.. literalinclude:: models.py
    :emphasize-lines: 4, 43, 46-47

This gives us the correct type on the dataclass instance's field.

What's happening behind the scenes?
``injected`` is a subclass of ``dataclasses.field`` which packs some information into the field metadata.
This metadata lets us give more instructions to the DI system.

Everything else in our app is the same, which shows our dataclasses can use DI to drive what they receive.