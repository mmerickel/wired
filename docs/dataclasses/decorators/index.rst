=======================
Decorators, Simple Case
=======================

.. note::

    Decorators depend on the ``venusian`` package being installed.

Our previous example didn't do Dependency Injection (DI) which makes it pretty boring. But it saved us from writing a factory function. Let's see how decorators can also save us the ``register_dataclass`` registration step.

Let's start with the one-time-only work in our "app", which bootstraps a registry and then looks for decorators:

.. code-block:: python

    import venusian
    from wired import ServiceRegistry

    def app_bootstrap():
        registry = ServiceRegistry()
        container = registry.create_container()
        scanner = venusian.Scanner(registry=registry)
        scanner.scan(__import__(__name__))

        return container

Our ``Greeter`` dataclass can now register itself as a ``wired`` factory, using a decorator:

.. code-block:: python

    from dataclasses import dataclass
    from wired.dataclasses import factory

    @factory()
    @dataclass
    class Greeter:
        name: str = 'Mary'

        def __call__(self, customer):
            return f'Hello {customer} my name is {self.name}'

We no longer need the call to the ``register_dataclass``, which needed the registry and the target class.
The decorator knows the registry, knows the class being decorated, and can call ``register_dataclass``.

As before, let's process an operation, this time with ``app_boostrap`` driving the decorator scanner:

Now your app can get instances from the container:

.. code-block:: python

    def main():

        container = app_bootstrap()
        instance = container.get(Greeter)
        greeting = instance('Larry')
        print(greeting)

Let's see if it works:

>>> main()
Hello Larry my name is Mary
