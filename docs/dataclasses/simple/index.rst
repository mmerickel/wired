===================
Simple Construction
===================

Before looking at injection, let's take a look at how dataclasses get registered, using a very simple example: a ``Greeter`` that greets people, for example in a store.

First, imagine we have a nice, boring ``Greeter``:

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Greeter:
        name: str = 'Mary'

        def __call__(self, customer):
            return f'Hello {customer} my name is {self.name}'

Since this is a ``wired`` application, we need a registry and a container:

.. code-block:: python

    from wired import ServiceRegistry

    registry = ServiceRegistry()
    container = registry.create_container()

Using ``wired`` directly, we'd define a factory function and register it:

.. code-block:: python

    def greeter_factory(container):
        greeter = Greeter()
        return greeter

    registry.register_factory(greeter_factory, Greeter)

With ``wired.dataclasses``, no factory function is needed, as it makes one for you:

.. code-block:: python

    from wired.dataclasses import register_dataclass

    # Make a new registry and container
    registry = ServiceRegistry()
    container = registry.create_container()

    register_dataclass(registry, Greeter)

Now your app can get instances from the container:

>>> instance = container.get(Greeter)
>>> greeting = instance('Larry')
>>> print(greeting)
Hello Larry my name is Mary

This was a very simple example: the ``Greeter`` needed nothing from its environment and thus, the only parts of "DI" used were construction of the dataclass instance.