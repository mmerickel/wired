=========
Overrides
=========

Here's one of the best parts of ``wired``, not seen in other Python plugin libraries/frameworks: not only can you extend, but you can *replace* (aka override) existing, core functionality.

In this sample the ``custom.py`` "add-on" continues to add a ``FrenchCustomer`` and a ``FrenchGreeter``.
But it also replaces the core ``Greeter`` with a different implementation.

As a further example of this, the ``test_overrides.py`` illustrates an extra, local re-definition.

Along the way, we refactor our the core dataclasses into a ``models.py`` file, to make it easier for the add-on to import without circular imports happening.

Code
====

``__init__.py``
---------------

.. literalinclude:: __init__.py

``custom.py``
-------------

.. literalinclude:: custom.py


``models.py``
-------------

.. literalinclude:: models.py
