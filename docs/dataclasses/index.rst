============
Dataclass DI
============

``wired`` can be used for Inversion of Control (IoC) to build a custom app with dependency injection (DI.)
But maybe you want to adopt an existing DI system? ``wired.dataclasses`` provides a DI system based on Python's
``datclasses`` and fields.

For example, the following dataclass gets the ``Settings`` from a ``wired`` registry:

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Greeter:
        settings: Settings
	
Or a decorator version which overrides the built-in ``Greeter`` for a ``FrenchCustomer`` and gets a single setting:

.. code-block:: python

    from dataclasses import dataclass
    from wired.dataclasses import injected, factory
    from .models import Greeter, FrenchCustomer

    @factory(for_=Greeter, context=FrenchCustomer)
    @dataclass
    class FrenchGreeter:
        punctuation: str = injected(Settings, attr='punctuation')

Simple Type-Based Injection
===========================

Let's take a look at the above example.
First, let's repeat it, but with the part that actually registers the dataclass:

.. code-block:: python

    from dataclasses import dataclass
    from wired.dataclasses import register_dataclass

    @dataclass
    class Greeter:
        settings: Settings

    # Presumes an existing registry instance
    register_dataclass(registry, Greeter)

This is equivalent to:

.. code-block:: python

    @dataclass
    class Greeter:
        settings: Settings

    # Presumes an existing registry instance
    def greeter_factory(container):
        settings: Settings = container.get(Settings)
        greeter = greeter(settings=Settings)
        return instance

    registry.register_factory(greeter_factory, Greeter)

In a nutshell, you didn't have to write a factory function.
Before explaining why, let's show an easier version, with decorators:

Decorators, Simple Case
=======================

.. note::

    Decorators depend on the ``venusian`` package being installed.

Our Greeter can skip the imperative ``register_dataclass`` using a decorator:

.. code-block:: python

    from dataclasses import dataclass
    from wired.dataclasses import factory

    @factory()
    @dataclass
    class Greeter:
        settings: Settings

We no longer need the call to the ``register_dataclass``, which needed the registry and the target class.
The decorator knows the registry, knows the class being decorated, and can call ``register_dataclass``.

How Does This Work?
===================

Dataclasses are useful in two ways:

- They have type annotations

- They have "fields"

``wired.dataclasses`` looks at each field, gets the type from the type annotation, and tries to get that type from the registry.
It does so for all the fields, then passes those in as arguments when constructing an instance of the dataclass.
This is all done inside a generic factory function.

Default Field Values
====================

Maybe your dataclass asks for a type that isn't in the registry.
Dataclass default values to the rescue:

.. code-block:: python

    from dataclasses import dataclass
    from wired.dataclasses import factory

    @factory()
    @dataclass
    class Greeter:
        greeting: str = 'Hello'

Why Does This Matter?
=====================

In traditional callback systems, like web frameworks, your functions are unwieldy.
For example, views accept a single argument -- ``request`` -- which has a rather infinite universe.

Wouldn't it be nice if all you had to do was ask for what you wanted, and they system was responsible for providing it?
This makes for far-less-coupled systems.
Especially systems with more than two parties.
Not just the web framework (or Sphix) and the site application, but plugins.

Passing around huge objects -- and worse, a ``g`` global of arbitrary
structure -- is a code smell and makes test-writing hard.
DI gives a much smaller surface area.

Containers
==========

Dataclass DI is usually done in the course of processing a unit of work, which usually means in a container.
Maybe you want to grab the container, then use ``__post_init__`` to pluck something out of the container:

.. code-block:: python

    from dataclasses import dataclass
    from typing import Optional

    from wired.dataclasses import factory

    from .models import Url

    
    @factory()
    @dataclass
    class Greeter:
        container: ServiceContainer
        url: Optional[str] = None

        def __post_init__(self):
            self.url = self.container.get(Url)

Yeh, that's kind of yucky.
We'll show an "attr" pattern later for this.	    

Overrides with ``for_`` and ``context``
=======================================

We have a ``Greeter`` that is used whenever our app asks for a ``Greeter``.
But maybe we want a second kind of ``Greeter``, used in a certain context.
For example, if we ask for a ``Greeter`` but the context is ``FrenchCustomer``, get a ``FrenchGreeter``.

Stated differently, we want:

- To register a ``FrenchGreeter``...

- To be used "for" ``Greeter``...

- ...when ``context is ``FrenchCustomer``

The imperative version would be this:

    from .models import Greeter, FrenchCustomer

    @dataclass
    class FrenchGreeter:
        settings: Settings

    # Presumes an existing registry instance
    register_dataclass(registry, FrenchGreeter,
                       for=Greeter, context=FrenchCustomer)

The decorator version, in this case, shows that ``factory`` takes those arguments:

    @factory(for_=Greeter, context=FrenchCustomer)
    @dataclass
    class FrenchGreeter:
        settings: Settings

With that, whenever someone asks for a ``Greeter``, if the current context is a ``FrenchCustomer``, they'll get ``FrenchGreeter`` instead.
		       
Injected
========

- What if you want a different type than the factory?

- E.e. ``customer: FrenchCustomer = injected(Context)``

Attributes
==========

Asking for ``Settings`` has two downsides:

- It's a pretty big surface area, maybe we only wanted a single value

- The single value we want probably isn't of type ``Settings``, it's probably a string.

``wired.dataclases`` provides a custom ``dataclass`` field called ``injected``:

    from wired.dataclasses import injected

    @factory()
    @dataclass
    class Greeter:
        greeting: str = injected(Settings, attr='greeting')

Behind the scenes this is the same as:

    from dataclasses import field

    @factory()
    @dataclass
    class Greeter:
        greeting: str = field(metadata=dict(injected=dict(type_=Settings, attr='greeting')))

Easier on the eyes.
	
The ``injected`` field uses the ``metadata`` support in dataclass fields to make a custom protocol, giving special instructions to the DI system on how to construct the dataclass.

For example, these two are equivalent:

    @factory()
    @dataclass
    class Greeter1:
        settings: Settings = injected(Settings)

    @factory()
    @dataclass
    class Greeter2:
        settings: Settings

With ``attr`` our DI contract with "the system" is more targeted.
Instead of asking for all of ``Settings``, we just get what we need.
Perhaps we want two things out of ``Settings``:

.. code-block:: python
		
    @factory()
    @dataclass
    class Greeter:
        greeting: str = injected(Settings, attr='greeting')
        punctuation: str = injected(Settings, attr='punctuation')

Custom Factories
================

It's nice using a generic factory that you don't have to write.
Sometimes you need more control and thus need a custom factory.
For example, you want to get a ``Customer`` from a ``Datastore`` based on the current ``url``.

Just leave a ``classmethod`` named ``wired_factory`` on your dataclass

Transitive Injection
====================

One thing can depend on another thing. For example, perhaps our Greeter greets a customer by name.
It ...needs the Customer, which might need the current Url from the container:

.. code-block:: python

    from .models import Context, Url, Settings

    @factory(for_=Context)
    @dataclass
    class Customer:
        url: str = injected(ServiceContainer, attr='url')
    @factory()
    @dataclass
    class Greeter:
        greeting: str = injected(Settings, attr='greeting')
        punctuation: str = injected(Settings, attr='punctuation')



Contents
========

- transitive DI

- request/resource/view patterns

- __call__

- wired_factory
  
- Collections aka queries
  
- Caching

- Context

    -
.. toctree::
   :maxdepth: 1

