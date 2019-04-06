=======
Context
=======

Now let's start showing off a little.

Sometimes you want a different kind-of-thing in certain contexts.
For example, a French-speaking Customer enters the store.
You might want a French-speaking Greeter.

``wired`` lets you register multiple flavors of things, stating *which* "context" determines which thing should be selected.
For example, give me a ``FrenchGreeter`` when the context is a ``FrenchCustomer``.
Magnifique!

This tutorial step shows this pattern:

- We register two factories, one without a context (the default) and one for the ``FrenchCustomer`` context

- Later, when a Customer comes in, we show selecting the Greeter based on "this is a French Customer" versus "nothing special about this Customer, just a default"

We also pass the Customer into the ``Greeter.__call__`` to let the Greeter greet the Customer by name.

Code
====

.. literalinclude:: app.py

