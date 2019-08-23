======
Simple
======


This is the simplest usage of ``wired``.
The store has one ``Greeter`` who always gives one kind of greeting.
The Greeter is a "singleton": there is only one, and we create it at startup time and re-use for the lifetime of the application.

Whenever a customer comes in, we make a "container" to do the work of the interaction.
We use the container to get from the registry all the piecesneeded.
(In this case, the only thing we need is the ``Greeter``.)

In this application, ``main`` shows:

- Wiring everything into a registry

- Later (and repeatedly), processing an interaction to greet a customer

This stuff in ``main`` would be the framework-y parts of your application.
Meaning, your application is responsible for making a registry, making a container, and "doing your thing" (greet a customer, process an HTTP request) within that container.

Code
====

.. literalinclude:: app.py
