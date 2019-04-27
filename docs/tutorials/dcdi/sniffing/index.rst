===============================
Getting Fields by Type Sniffing
===============================

We're doing dependency injection, but the app-builders consuming our application have to manually get stuff from the registry.
Let's look at a pattern like Angular, where constructors put types on their arguments and "the system" finds the right object to pass in.

This approach increases the level of "magic".
OTOH, it's obviously easier to use.
It can also fix two annoyances with the typical callback-based system:

- The callee (e.g. a view) has to provide every function argument the caller might ever provide, leading to a lot of cases of "unused argument"

- We wind up packing the universe into a ``request`` object, which then has an impossibly-large surface area

With this kind of approach, each callee specifies only what it needs.
The caller finds what it asks for and provides it.

This example is done as dataclasses, which are a thin layer of automation atop a ``__init__`` constructor.
This pattern works for regular functions and methods, as we'll see in a moment.

Dataclasses though are interesting for this:

- They already embrace type annotations, duh

- The ``field`` concept gives a layer of abstraction not available in regular "list of function arguments" which we can put to use in dependency injection

- One could imagine persisting the dataclass between calls

Along the way, we did some refactoring:

- We make the settings available in the container as a singleton

- We then drop them from the add-ons "setup" protocol, since add-ons can get the settings from the registry if they want them

- Moved some framework-y parts to a ``utils.py`` file, so that ``__init__.py`` is easier to reason about

- Each factory function is moved to a ``staticmethod`` on the class that is being registered, simulating a decorator that could automate this

Code
====

``__init__.py``
---------------

.. literalinclude:: __init__.py

``models.py``
-------------

.. literalinclude:: models.py

``custom.py``
-------------

.. literalinclude:: custom.py

``utils.py``
------------

.. literalinclude:: utils.py
