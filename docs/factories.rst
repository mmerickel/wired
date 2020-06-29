=========
Factories
=========

The Simplest Case
=================

Let's say we have a service that needs nothing from the container.
It just provides a way to find the service:

.. code-block:: python

    class LoginService:
        def __init__(self):
            ...
    def login_factory(container: ServiceContainer) -> LoginService:
        return LoginService()
    registry.register_factory(login_factory, LoginService)

While this looks absurd -- "why do I need a service for this, just construct an instance" -- there's actually some utility:

- A pluggable app could allow replacing the built-in ``LoginService``

- If it did, it could have access to the container and pull in dependent data it might need

- You could have multiple ``LoginService`` factories, each for a different context

With the *new* factory proposal, this would simply be:

.. code-block:: python

    registry.register_factory(login_factory, LoginService)

Behind the scenes a callable would be generated that collected the container and, in this case, discarded it.

There will also be a decorator version:

.. code-block:: python

    @wired_factory()  # Could also pass for_=BaseLogin, context=SomeContext, etc.
    class LoginService:
        def __init__(self):
            ...

In this case, the ``for_`` defaults to the decorated class.

Using The Container
===================

Let's say the login service needed something from the container.
In the example in usage, ``LoginService`` needs to get the ``Session`` from the container.
The example used lookup-by-name but we'll use lookup-by-type:

.. code-block:: python

    class LoginService:
        dbsession: Session
        def __init__(self, container: ServiceContainer):
            self.dbsession = container.get(Session)

And...that's it.
The previous ``register_factory`` and ``@wired_factory`` both work.
How?
The check to see if the callable's signature asks for an argument of type ``ServiceContainer``, and if so, the container is passed in.
This matches the original ``wired`` service contract, in which the factories were passed a container (even if they didn't want it.)

You don't have to use classes: any callable will do.
Here's a function-oriented variation:

.. code-block:: python

    class LoginService:
        dbsession: Session
        def __init__(self, dbsession: Session):
            self.dbsession = dbsession
            
    @wired_factory()
    def login_factory(container: ServiceContainer) -> LoginService:
        dbsession = container.get(Session)
        return LoginService(dbsession)

Interesting changes here:

- The class constructor is passed just the data that it needs, rather than the (large-surface-area, wired-specific) container
- The function's return type hint is used as the ``for_`` in the registration

You might be asking yourself: "Hmm, that looks a little like dependency injection."
And you'd be right!
It's just a special case of what we'll discuss in a bit.
But first, let's formalize the case above.

Controlling the Construction
============================

In the last case above, we needed to get some data from the container, so we wrote a function -- quite like what we did in the original *Usage* example.
We were just able to skip the ``registry.register_factory`` step by using a decorator.

What if we gave classes a protocol for controlling the construction process?
Enter the ``__wired_factory__`` class method:

.. code-block:: python

    @wired_factory()
    class LoginService:
        dbsession: Session
        def __init__(self, dbsession: Session):
            self.dbsession = dbsession
            
        @classmethod
        def __wired_factory__(cls, container: ServiceContainer):
            dbsession = container.get(Session)
            return cls(dbsession=dbsession)

The ``for_`` used defaults again to the class.

The imperative form, instead of a decorator:

.. code-block:: python

    registry.register_factory(LoginService)

Simple DI By-Type
=================

That's nice, but it's still a bit of boilerplate.
The new factory support handles dependency injection in a variety of useful ways.
Let's show how the class can simply say "Give me the Session":

.. code-block:: python

    @wired_factory()
    class LoginService:
        dbsession: Session
        def __init__(self, dbsession: Session):
            self.dbsession = dbsession

In this case, the constructor's (one) argument was a type that is registered as a service.
``@wired_factory`` sniffed at the argument type, did a ``container.get()``, and used that as the constructor argument.

Let's see a dataclass flavor of that, to reduce the boilerplate even more:

.. code-block:: python

    @wired_factory()
    @dataclass
    class LoginService:
        dbsession: Session

Again, this works with either the ``@wired_factory`` decorator or the imperative ``register_factory``.
Injection also works with functions:

.. code-block:: python

    @factory
    def login_factory(dbsession: Session) -> LoginService:
        # Potentially do some work here
        return LoginService(dbsession=dbsession)

Maybe "Potentially do some work here" means access to the container.
If so, just ask for it as well:

.. code-block:: python

    @wired_factory()
    def login_factory(container: ServiceContainer, dbsession: Session) -> LoginService:
        # Potentially do some work here
        return LoginService(dbsession=dbsession)

Argument order doesn't matter:

.. code-block:: python

    @wired_factory()
    def login_factory(dbsession: Session, container: ServiceContainer) -> LoginService:
        # Potentially do some work here
        return LoginService(dbsession=dbsession)

A DSL for Injection: Type Changing
==================================

*Note: This might be where the default injector parts ways with a ``@wired_dataclass`` or ``__wired_factory__`` add-on.*

The container's context is a useful thing to have in a service.
The DI story makes this easy, using the ``Context`` marker which flags the injector to get ``container.context``:

.. code-block:: python

    @wired_factory()
    @dataclass
    class Greeting:
        customer: Context

        def __call__(self) -> str:
            return f'Hello {self.customer.name}'

That's great, but sometimes we know the context is a ``Customer`` and we want to use that in the type hint.
It would be nice if we could tell *Python* one type hint, but use another type for injection.

Let's use PEP 593 "Flexible Annotations".
``wired`` would add:

.. code-block:: python

    Injector = object()
    LT = TypeVar("local_type")
    RT = TypeVar("registered_type")
    Injected = Annotated[LT, RT, Injector]

Now a user could write:

.. code-block:: python

    @dataclass
    class Customer:  # container.context is an instance of this
        name: str

    @wired_factory(context=Customer)
    @dataclass
    class Greeting:
        customer: Injected[Customer, Context]

With this PEP 593 syntax, the ``Greeting.customer`` field winds up with a type of ``Customer``.
The extra information -- ``Context`` -- is ignored by everything in the universe *except* wired's injector.
It does the following:

- Look for the first field ``customer``
- Get the type information
- See that it is ``Annotated``
- See that the alias's annotation has the ``Injector`` marker telling the injector to pay attention
- Get the second value and use it as the container lookup

In a perfect world, this whole dance is itself a service, meaning everything is cached per-container after the first lookup.

The earlier version of ``wired`` relied on dataclass field metadata to leave behind these signals.
Thanks to PEP 593, we can do the same for functions:

.. code-block:: python

    @wired_factory()
    def greeting_factory(customer: Injected[Customer, Context]) -> LoginService:
        # Potentially do some work here
        return Greeting(customer=customer)

Injector DSL: Attributes
========================

The earlier ``wired`` dataclass injector solved an additional problem.

Our ``Greeting`` gets a ``Customer``.
It can then have a method that says hello, e.g. ``f'Hello {self.customer.name}'``.
But that's a big surface are -- the entire ``Customer`` -- when the contract really only wants one piece of data.

The earlier support allowed a field value of ``injector(Context, attr='name')``.
This new, ``Annotation``-based injector supports that case and more:

.. code-block:: python

    @wired_factory(context=Customer)
    @dataclass
    class Greeting:
        customer_name: Injected[str, Context, Attr('name')]


What is ``Attr``?
Think of it as kind of an adapter or filter.
Which means, you can plug in any kind of callable there.
In fact, one could imagine a chain of "Injector DSL" adapter-thingies, as long as there's a protocol for passing the result of one to the input of another.

.. code-block:: python

    @wired_factory(context=Customer)
    @dataclass
    class Greeting:
        customer_name: Injected[str, Context, Chain(Attr('english_names'), Key('first_name')]

These ``Chain`` predicates could act like a database query, filtering the result set from a source:

.. code-block:: python

    @wired_factory(context=Customer)
    @dataclass
    class Greeting:
        customers: Injected[Tuple[Customer], AllCustomers, Chain(Filter(status='active'), Batch(10))]

In fact, this pattern matches ``Rx`` and other observable-style libraries.
What's nice is that, like Pyramid predicates, these don't have to be in the core.

Custom DI
=========

We discussed above how the ``__wired_factory__`` protocol let classes control how they were constructed.
And now that we've seen DI, it should come as no surprise that this method itself can use DI:

.. code-block:: python

    @wired_factory()
    class LoginService:
        dbsession: Session
        def __init__(self, dbsession: Session):
            self.dbsession = dbsession

        @classmethod
        def __wired_factory__(cls, dbsession: Session):
            return cls(dbsession=dbsession)

But what if we had an application with some particular DI requirements?
You could make all of your services implement the protocol, but that's cumbersome.
You could move that to a base class, but that violates the spirit of composition over inheritance.

Instead, move the custom-construction bits to an intermediate decorator:

.. code-block:: python

    @wired_factory()
    @wired_dataclass()
    class LoginService:
        dbsession: Session
        def __init__(self, dbsession: Session):
            self.dbsession = dbsession

This decorator would do nothing more than stamp -- dynamically -- a ``__wired_factory__`` class method onto the decorated class.

Further ideas: a custom injector which recorded the connection to a service, then pushed updates to instances when the service changed.
Sort of like pub-sub.

Props
=====

``wired`` is being used as part of a component system based on ``htm.py`` and ``viewdom``.
In a nutshell:

.. code-block:: python

    @component()
    @dataclass
    class Greeting:
        name: str
        punctuation: Injected[str, Config, Attr('punctuation')]

        def __call__(self) -> VDOM:
            return html('<div>Hello {self.name}{self.punctuation}'

    # In some template somewhere, where the "props" are dict(name='Paul')
    html('<section><{Greeting} name="Paul" /></section>')

In normal cases, construction can get arguments from field default values or the container.
But the above adds another source, one that is checked first: "props".
This dict of data needs to get into the injection.

Currently this is done by a fork of ``Injector`` with a ``__call__`` that gets ``**kwargs``.
It will be interesting to see where this moves.
I briefly considered doing a container clone at each component boundary, and stashing the props in the container.
But that would mean *lots* of containers get created during a "request".
