.. skip: start

==========
Attributes
==========

Now the fun begins.
The ``injected`` field uses metadata to give more instructions to the DI system.
Let's put that to work to decrease the surface area between the dataclass and the system by getting just what we need off of ``Customer``.

We'll change 4 lines in ``models.py`` and nothing else:

.. literalinclude:: models.py
    :emphasize-lines: 31, 36, 44, 49

Instead of storing the ``Customer`` and later getting the customer's name, we use ``attr`` to get just the ``name`` off the ``Context``.
The dataclass then has ``customer_name: str`` as its constructed field, which is the only thing needed in the "template".
Smaller surface are against the outside world.

Here is what ``wired.dataclasses`` actually does behind the scenes:

.. code-block:: python

    from dataclasses import field

    @factory()
    @dataclass
    class Greeter:
        customer_name: str = field(metadata=dict(injected=dict(type_=Context, attr='name')))

Using ``injected`` with an argument is easier on the eyes.
The ``injected`` field uses the ``metadata`` support in dataclass fields to make a custom protocol, giving special instructions to the DI system on how to construct the dataclass.

.. note::

    ``attr`` isn't the only argument you can add to ``injected``. ``key=`` also works for dictionary access.
