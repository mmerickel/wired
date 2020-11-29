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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll now move the ``Greeter`` class to also use the ``@service_factory`` decorator instead of a manual registration.
Since it hard-codes ``Marie`` as a value to the constructor, we use the ``__wired_factory__`` protocol as a class method to generate the instance.
This means any code that does ``container.get(Greeter)`` will run this class method to construct the ``Greeter``.

.. literalinclude:: ../examples/decorators/decorator_with_wired_factory.py

We also add a ``__wired_factory__`` class method to ``Greeting`` to make it nicer.
Now its constructor no longer uses the ``container``, which is a huge surface area.
Instead, the class is constructed just with the data it needs, which is nice for testing.
The class method acts as an "adapter", getting stuff out of the container that is needed for the class.


.. _examples-wired-factory:

Wired Factory
~~~~~~~~~~~~~

