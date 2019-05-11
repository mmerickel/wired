.. skip: start

=======================
Decorators, Simple Case
=======================

.. note::

    Decorators depend on the ``venusian`` package being installed.

Our previous example didn't do Dependency Injection (DI) which makes it pretty boring. But it saved us from writing a factory function. Let's see how decorators can also save us the ``register_dataclass`` registration step.

Let's start with the one-time-only work in our "app", which bootstraps a registry and then looks for decorators:

.. literalinclude:: ../../tests/dataclasses/integration/decorators/app.py

Our ``Greeter`` dataclass can now register itself as a ``wired`` factory, using a decorator:

.. literalinclude:: ../../tests/dataclasses/integration/decorators/models.py

We no longer need the call to the ``register_dataclass``, which needed the registry and the target class.
The decorator knows the registry, knows the class being decorated, and can call ``register_dataclass``.

As before, let's process an operation, this time with ``app_boostrap`` driving the decorator scanner:

Now your app can get instances from the container:

.. code-block:: python

    # This happens at app startup
    registry = make_registry()

    # This happens on each operation
    result = process_request(registry)
    assert 'Hello Larry my name is Mary' == result
