=========
Datastore
=========


Sharp readers will have spotted the flaw in ``decoupled``: the main application had to know about and create a ``FrenchCustomer``.
We want the add-on to be the only place that knows about.

Let's make a mini-database of Customers and let the add-on create and store a FrenchCustomer.
The main app is then blissfully unaware...it just knows to that a Customer has a type and a name.

We do this by making a ``Datastore`` dataclass and registering an instance as a singleton.
This lets all service factories fetch the Datastore.

Along the way we did some refactoring to make the call sequence better match how an application like this should work:

- ``greet_customer`` doesn't make its own container, instead, one is made in the core of the app

- Rename ``greet_customer`` to ``customer_interaction`` to connote this might be more steps than just a greeting

- Change the functions to receive a container (for the interaction/request) rather than the entire registry

- Rename the ``__init__.setup`` function to ``app_bootstrap`` to make it more clear what it's doing

- Move some of its responsibility to a ``setup`` function to match the add-on setup, thus the core isn't "special"

- Refactor sample interactions out of ``main`` to make testing simpler, then decrease the test to just one integration-style test (these are sample applications, no need for unit tests)

Code
====

``__init__.py``
---------------

.. literalinclude:: __init__.py

``custom.py``
-------------

.. literalinclude:: custom.py
