========
Tutorial
========

Let's write a ``wired`` application using inversion of control (IoC).

.. note::

    This tutorial uses dataclasses. Why? Why not? [wink]
    There's nothing in the core of ``wired`` that *requires* type hints, dataclasses, etc., although ``wired`` does ship with a dependency injection system based on dataclasses.

Our application will be a ``Greeter``.
Someone walks in a store, they get greeted.
We'd like IoC to help us make this into a *decoupled*, *extensible*, *configurable*, *pluggable* application.

- We might want to change the ``Greeter``

- The ``Greeter``'s greeting has punctuation...maybe that is in a config file

- We might want a ``Customer`` who receives the greeting

- We might want a ``FrenchGreeter`` for a ``FrenchCustomer``

- Each ``Customer`` comes from a "datastore"..let's make that transparent and pluggable

- Some people might not like our decisions...let's show how to *replace* built-in stuff, in *certain* (unlike other Python plugin systems which focus on *adding* stuff)

- Finally, let's make it look like the patterns we see in web frameworks

.. raw:: html

    <h2>Tutorial Steps</h2>

.. toctree::
   :maxdepth: 1

   simple/index
   factory/index
   settings/index
   context/index
   decoupled/index
   datastore/index
   overrides/index
   requests_views/index