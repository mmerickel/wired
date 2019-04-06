=========
Decoupled
=========


``wired`` lets you register different flavors of a thing.
Above we had a ``Greeter`` and a ``FrenchGreeter``.
This pattern is useful when making an *extensible* application: Other packages can add flavors of things that match in custom circumstances.

In this sample we change the application from a single file into a package.
In ``decoupled/__init__.py`` we make the "default" application.
It only knows about Customer and Greeter. In ``custom.py`` we simulate an installed add-on package which adds ``FrenchCustomer`` and ``FrenchGreeter``.
``custom.py`` has a ``setup`` function which wires itself up.

*This* application's protocol is:

- If your package has a ``setup`` function at the top level...

- ..then we'll call it, passing the registry and the settings

Same functionality as the ``context``, but simulating an add-on package.

Code
====

``__init__.py``
---------------

.. literalinclude:: __init__.py

``custom.py``
-------------

.. literalinclude:: custom.py