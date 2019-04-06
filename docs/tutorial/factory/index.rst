=======
Factory
=======

This time our Greeter is a factory.
Each time a Customer comes in, we make the Greeter.
(Don't worry, behind the scenes there is a cache.)

Changes
=======

- Setup gains a ``greeting factory`` function which is registered in the registry

- This function constructs the ``Greeter``

- It's registered with ``register_factory`` instead of ``register_singleton``

- That's it...our code doesn't know, when it asks for a ``Greeter``, that it came from a factory instead of a singleton

Code
====

.. literalinclude:: app.py

