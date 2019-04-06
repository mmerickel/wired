========
Settings
========

Sometimes our factories (and even singletons) need some configuration settings from the outside system.
``wired`` doesn't have or need any special machinery for that, but it's a common pattern, so here's an example.

With this, our entities -- Greeter, Customer, etc. -- can be setup with values for a particular "store".
We'll see in a later example why it is useful to have decoupled, arms-length configuration and registration.

Code
====

.. literalinclude:: app.py

