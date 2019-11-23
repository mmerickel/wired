=======================================
Automating Registration with Decorators
=======================================

We're missing two things at the moment in our developer experience: decorators and a delayed configuration system.
Both can help solve some boilerplate and repetition in our code.

We'll use the ``venusian`` package to give us both.
From this point forward the examples presume that ``venusian`` is installed.

With this change, things become really dead-simple to use.
The framework can use its own factory function for the simple case while giving dataclasses the option to provide a method.
This default factory can construct instances simply by finding what they want, getting those values, and passing into the constructor.

Along the way, some refactoring:

- The ``factory`` staticmethod is renamed ``wired_factory``

- Added a ``FrenchView`` to show getting a different View in the case of a certain kind of Customer (a FrenchCustomer)


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

``decorators.py``
-----------------

.. literalinclude:: decorators.py
