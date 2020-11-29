========
Examples
========

.. _examples-decorators:

Decorators
~~~~~~~~~~

Let's show the use of `venusian <https://pypi.org/project/venusian/>`_ and the :class:`wired.service_factory` decorator in building an app that scans for factories.
We'll do it piece-by-piece, starting with a regular ``wired`` app.

Basic ``wired`` app
-------------------

As a starting point we use an app with *no* decorators.
In this app we have a ``Greeting`` class that depends on a ``Greeter`` class.
As such, we register a factory for each.

.. literalinclude:: ../examples/decorators/no_decorator.py

This is the basics of a simple, pluggable application.
As a note, everything in the ``app`` function would typically be done once as part of your app.

Class as factory
----------------

Before getting to decorators, just to emphasize...the first argument to :meth:`wired.ServiceRegistry.register_factory` can be the class itself.

.. literalinclude:: ../examples/decorators/no_decorator_class.py
    :emphasize-lines: 25

``venusian`` scanner
--------------------

We will now add ``venusian`` and its ``Scanner``.
We make a ``Scanner`` instance and include the ``registry``.
When we call ``scan`` on a module -- in this case, the same module -- it looks for the ``@service_factory`` decorator.
The decorator then extracts the ``registry`` instance we stored in the ``Scanner`` and does the registration.

.. literalinclude:: ../examples/decorators/basic_class.py

What's nice about this venusian approach: no module-level state globals stuff.

Another decorator plus ``__wired_factory__``
--------------------------------------------

We'll now move the ``Greeter`` class to also use the ``@service_factory`` decorator instead of a manual registration.
Since it hard-codes ``Marie`` as a value to the constructor, we use the ``__wired_factory__`` protocol as a class method to generate the instance.
This means any code that does ``container.get(Greeter)`` will run this class method to construct the ``Greeter``.

.. literalinclude:: ../examples/decorators/decorator_with_wired_factory.py

We also add a ``__wired_factory__`` class method to ``Greeting`` to make it nicer.
Now its constructor no longer uses the ``container``, which is a huge surface area.
Instead, the class is constructed just with the data it needs, which is nice for testing.
The class method acts as an "adapter", getting stuff out of the container that is needed for the class.

Decorator arguments
-------------------

The ``@service_factory`` acts as a replacement for ``register_factory``.
Thus it needs to support the other arguments beyond the first one:

- The ``service_or_iface``, if not provided, defaults to the class the decorator is decorating
- If you pass ``for_=`` to the decorator, it will be used as the ``service_or_iface`` argument to
- You can also pass ``context=`` and ``name=``

Imagine our app now has a ``Customer`` and ``FrenchCustomer`` as container contexts.
Here is an example of registering different ``Greeter`` classes that are unique to those contexts:

.. literalinclude:: ../examples/decorators/decorator_args.py

.. _examples-wired-factory:

Wired Factory
~~~~~~~~~~~~~

Registering a factory means two things: a callable that constructs and returns an object, then the "kind" of thing the factory is registered for.
You can eliminate the callable as a separate function by providing a ``__wired_factory__`` callable *on*, for example, the class that gets constructed.

This is the wired factory "protocol" and the callable acts as an adapter.
It is handed the container, extracts what it needs, then constructs and returns an object.

Basic wired factory callable
----------------------------

We start again with our simple app, with a ``Greeting`` that uses a ``Greeter``.
In this case, we do two things:

- Both classes have a ``classmethod`` that manages construction of instances
- The ``register_factory`` first argument is, thus, the class itself

.. literalinclude:: ../examples/wired_factory/register_wired_factory.py

With this, when some application code calls ``container.get(Greeter)``, the construction is done by ``Greeter.__wired_factory__``.

