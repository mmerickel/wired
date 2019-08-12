.. skip: start

===================
Simple Construction
===================

Before looking at injection, let's take a look at how dataclasses get registered. We'll use a very simple example: a ``Greeter`` that greets people, for example in a grocery store.

First, imagine we have a nice, boring ``Greeter``:

.. literalinclude:: models.py

Since this is a ``wired`` application, we need an application with a registry. Dataclasses are fun, let's use them for our application:

.. literalinclude:: app.py

During startup, we create the app (and thus registry) and then start configuring our stuff. For example, here is a configuration step:

.. literalinclude:: configure.py

If we were using ``wired`` directly, we would have to define a factory function and register it:

.. code-block:: python

    # NO LONGER NEED THIS, wired.dataclasses makes a factory
    def greeter_factory(container):
        greeter = Greeter()
        return greeter

    registry.register_factory(greeter_factory, Greeter)

But with ``wired.dataclasses``, no factory function is needed, as `wired.dataclasses` makes a factory for you

The application is now finished starting up. Later on, it's time to process a "request". Here's a function that can do so:

.. literalinclude:: request.py


Now let's put all these pieces together: models, application, configuration, and request processing:

.. literalinclude:: ../../../tests/dataclasses/integration/test_dc_simple_construction.py
    :start-after: start-after

This was a very simple example: the ``Greeter`` needed nothing from its environment because the only field had a default value. Thus, the only parts of "DI" used were construction of the dataclass instance.