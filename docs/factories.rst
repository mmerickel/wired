=========
Factories
=========

The first versions of ``wired`` had a simple factory registration protocol:

- Provide a callable and a class/interface to register for
- That callable gets passed the container and returns the class/interface "instance"

This can be streamlined and expanded.

Current Implementation
======================

Imagine a ``LoginService``:

.. code-block:: python

    class LoginService:
        def __init__(self):
            ...

With ``wired``, you have a factory function that can get information from the container, construct an instance, and return it:

.. code-block:: python

    def login_factory(container):
        return LoginService()

In the existing ``wired``, registering a factory means is a method call on the registry:

.. code-block:: python

    registry.register_factory(login_factory, LoginService)

Thus, the first parameter is the factory function and the second is the "type" it is registering to handle.
This is a simplified example:

- ``register_factory`` doesn't *have* to take a second argument -- it can default to ``Interface`` which basically means "anything".

- The ``register_factory`` method also exists on ``ServiceContainer`` but that's a detail.

For such a simple case, the ``login_factory`` function isn't really needed.
In fact, several pieces can be streamlined, especially in the presence of decorator support and type hinting.
Let's take a look.

The Simplest Case
=================

The above -- contrived -- example just constructs a class.
Meaning, the class *constructor* is entirety of the factory.
Imagine eliminating the ``def login_factory`` function and just doing this directly:

.. code-block:: python

    registry.register_service(LoginService)

How might that work?
``registry.register_service`` might look like this:

.. code-block::

    def register_factory(
        self, factory, iface_or_type=Interface, *, context=None, name=''
    ):

        if len of args is 2 and it is the same args:
            do the existing thing
        elif it is one arg and it is a class:
            def _factory(container):
                return iface_or_type()
            do the existing thing, but with _factory in place of factory

Meaning, make a small closure function and return it.
There's nothing unique from registration to registration in this case: they all have the same no-op factory function of `_factory`.
The only real work is in sniffing the ``register_factory`` arguments and detection which path to go on.
For example, ``register_factory`` accepts to keyword-only arguments: ``context`` and ``name``.

TODO Need some help simplifying the signature
TODO Can functools help here? Curried functions and partials and the like?

Decorator Version
=================

This simplification gets even more attractive in the presence of a decorator-based registration:

.. code-block:: python

    @wired_factory
    class LoginService:
        def __init__(self):
            ...

The existing -- and soon to be re-invented -- dataclass decorator support uses ``venusian`` with a bound registry and a local closure.
This ``wired_factory`` decorator would work similarly.

The decorator could also support other arguments to match ``register_factory``:

.. code-block:: python

    @wired_factory(for_=LoginService, context=FrenchCustomer)
    class FrenchLoginService:
        def __init__(self):
            ...

In this case we are adding a second registration for ``LoginService``, to be used in the case where the container's context is a ``FrenchCustomer``.
A similar syntax could be used for the ``name`` keyword argument.

Custom Factory Logic
====================

These changes work well for the simplest case: no logic, nothing needed from the container.
But that's not really what ``wired`` is about: factories are places where domain logic and container state is used for construction.

Let's add a protocol to let the class manage its construction:

.. code-block:: python

    class LoginService:
        def __init__(self, customer_name):
            self.customer_name = customer_name

        @classmethod
        def __wired_factory__(cls, container: ServiceContainer):
            customer = container.get(Customer)
            customer_name = customer.name
            return cls(customer_name)

We now register this, as before:

.. code-block:: python

    registry.register_service(LoginService)

The pseudo-code for ``register_factory`` changes a little, to sniff for the protocol:

.. code-block::

    def register_factory(
        self, factory, iface_or_type=Interface, *, context=None, name=''
    ):

        if len of args is 2 and it is the same args:
            do the existing thing
        elif it is one arg and it is a class:
            if iface_or_type has ``__wired_factory__``:
                _factory = iface_or_type.__wired_factory
            else:
                def _factory(container):
                    return iface_or_type()
            do the existing thing, but with _factory in place of factory

The logic then is pretty simple:

- If the class has a "factory", use it

- Otherwise, it's the simple case, and make a simple function to act as the factory

Just to be clear, with a decorator, no ``registry.register_service`` is needed:

.. code-block:: python

    @wired_factory
    class LoginService:
        def __init__(self, customer_name):
            self.customer_name = customer_name

        @classmethod
        def __wired_factory__(cls, container: ServiceContainer):
            customer = container.get(Customer)
            customer_name = customer.name
            return cls(customer_name)

.. note::

    If this looks like it is paving the way for the injector, it's because it is
    paving the way for the injector. [wink]

Registering a Function With Return Type
=======================================

Perhaps you need some custom construction but you don't control the class and can't add ``__wired__factory__``.
In such a case, register the function, not the type:

.. code-block:: python

    def make_login_service(container) -> LoginService:
        customer = container.get(Customer)
        customer_name = customer.name
        return LoginService(customer_name)

    registry.register_service(make_login_service)

Ah, this is interesting!
``register_factory`` knows that it is passed a callable with a return type hint.
It detects that case and does the equivalent of ``registry.register_service(make_login_service, LoginService)``.
As such, it's a shorthand.

It's more useful in the decorator form:

.. code-block:: python

    @wired_factory
    def make_login_service(container) -> LoginService:
        customer = container.get(Customer)
        customer_name = customer.name
        return LoginService(customer_name)

If the decorator was passed ``for_`` as an argument, it would register with that ``iface_or_type`` instead.

Registering a Function Ignoring Return Type
===========================================

.. note::

    This one is obsolete.
    Even if Michael wanted to do it, there isn't really a way to do it when combined with the above, as functions will want to type hint their return values.
    Instead, I will scratch this itch with a specialty decorator e.g. ``@component`` which ignores the return type hint and defaults to a ``for_`` matching the function name.

Let's say you have a greeting system where a function can return a string.
The string, though, has data from the container:

.. code-block:: python

    def Greeting(container):
        customer = container.get(Customer)
        config = container.get(Configuration)
        return f'Hello {customer.name}{config.punctuation}'

This one is an odd duck: it just returns a string.
It has no type hint for a return type.
But is can be very useful in systems that embrace functional programming, such as component systems.

With this, if you then did the following registration, you could get the following with a lookup:

.. code-block:: python

    registry.register_service(Greeting)
    # Register Customer and Configuration factories
    container = registry.create_container()
    greeting = container.get(Greeting)
    assert greeting == 'Hello Maria!'
