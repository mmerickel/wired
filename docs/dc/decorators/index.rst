=======================
Decorators, Simple Case
=======================

.. note::

    Decorators depend on the ``venusian`` package being installed.

Our previous example didn't do Dependency Injection (DI) which makes it pretty boring. But it saved us from writing a factory function. Let's rewrite it to see how decorators can also save us the ``register_dataclass`` registration step. Still no DI.

As before, we have an application with a registry. Let's add a method that looks for our ``wired.dataclasses`` decorators, using ``venusian``:

.. literalinclude:: app.py
    :emphasize-lines: 11-15

Our ``Greeter`` dataclass can now register itself as a ``wired`` factory, using a decorator:

.. literalinclude:: models.py
    :emphasize-lines: 7

We no longer need the call to the ``register_dataclass``, which needed the registry and the target class.
The decorator knows the registry, knows the class being decorated, and can call ``register_dataclass``. Simple!

Our request processing is exactly the same as the previous step:

.. literalinclude:: request.py

Putting it all together: make an app, scan for decorators, and process requests:

.. literalinclude:: ../../../tests/dataclasses/integration/test_dc_decorators.py
    :start-after: start-after

