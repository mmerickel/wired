============
Dataclass DI
============

``wired`` can be used for Inversion of Control (IoC) to build a custom app with dependency injection (DI.)
But maybe you want to adopt an existing DI system? ``wired.dataclasses`` provides a DI system based on Python's ``datclasses`` and fields.

For example, a dataclass that needs the ``Settings`` from a ``wired`` registry:

.. invisible-code-block: python

    from dataclasses import dataclass
    from wired.dataclasses import injected, factory

    class Settings:
        pass

    class FrenchCustomer:
        pass

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Greeter:
        settings: Settings

``wired.dataclass`` handles the instantiation of that dataclass for you by getting ``Settings`` from the container.

Or a decorator version which overrides the built-in ``Greeter`` for a ``FrenchCustomer`` and gets a single setting:

.. code-block:: python

    @factory(for_=Greeter, context=FrenchCustomer)
    @dataclass
    class FrenchGreeter:
        punctuation: str = injected(Settings, attr='punctuation')

Why Is This Interesting?
========================

``wired`` provides a library for Inversion-of-Control (IoC.) You can use this to write your own dependency injection system. Or you can use ``wired.dataclasses``, an optional part of ``wired`` targeting Python 3.7+ (or using the 3.6 backport of dataclasses.)

Also, you don't need to write a factory function. ``wired.dataclasses`` does this for you. (Though you can provide your own in a class method.)

Since you are delegating to ``wired.dataclasses`` much of the work of finding the right data and using it to construct your objects, you have fewer tests to write.

Next, ``wired.dataclasses`` works really hard to minimize the surface area of your objects, and thus with the outside system. If your dataclass can get constructed, it's good.

Finally, with the optional decorator support, ``wired.dataclasses`` further decreases the boilerplate by automating the imperative registration.

Later on, ``wired.dataclasses`` might provide some interesting caching...both of the dataclass instance and the result of its ``__call__``.

How Does This Work?
===================

Dataclasses are useful in two ways:

- They have type annotations

- They have "fields"

``wired.dataclasses`` looks at each field, gets the type from the type annotation, and tries to get that type from the registry.
It does so for all the fields, then passes those in as arguments when constructing an instance of the dataclass.
This is all done inside a generic factory function.

Why Does This Matter?
=====================

In traditional callback systems, like web frameworks, your functions are unwieldy.
For example, views accept a single argument -- ``request`` -- which has a rather infinite universe.

Wouldn't it be nice if all you had to do was ask for what you wanted, and they system was responsible for providing it?
This makes for far-less-coupled systems.
Especially systems with more than two parties.
Not just the web framework (or Sphinx) and the site application, but plugins.

Passing around huge objects -- and worse, a ``g`` global of arbitrary structure -- is a code smell and makes test-writing hard.
DI gives a much smaller surface area.

Contents
========

.. toctree::
    :maxdepth: 1

    usage
    API <api>