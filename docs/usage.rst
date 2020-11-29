=====
Usage
=====

The basic workflow is:

1. Create a :class:`wired.ServiceRegistry` containing service factories and
   service singletons.

2. Invoke :meth:`wired.ServiceRegistry.create_container` per logical operation to create a :class:`wired.ServiceContainer` object.

3. Invoke :meth:`wired.ServiceContainer.get` as necessary to get a service instance conforming to the desired name/interface.

::

                                                 ┌───────────────────────┐
                                                 │                       │
                                      ┌──────────│    ServiceContainer   │
                                      │          │                       │
                                      │          └───────────────────────┘
                                      │
  ┌──────────────────────┐            │                     ■
  │                      │            │
  │    ServiceRegistry   │<───────────┤                     ■
  │                      │            │
  └──────────────────────┘            │                     ■
                                      │
                                      │          ┌───────────────────────┐
                                      │          │                       │
                                      └──────────│    ServiceContainer   │
                                                 │                       │
                                                 └───────────────────────┘

Registering services
--------------------

Service singletons and factories can be registered by type or by name.
It is recommended to register them by type to avoid naming clashes.
Two services registered for ``name='login'`` would clash and it would be unclear what each one is.
However, a service factory that is registered to provide instances of the ``LoginService`` class are unambiguous.
Anyone else registering such a service factory is directly competing for control of that type.
It is possible to register for both type and name.

As a note, when calling :meth:`wired.ServiceRegistry.register_factory`, the first argument is a callable.
It doesn't have to be a function: it could be a class that accepts the container as an argument.
In such a case, the class might be *both* arguments.
This kind of usage is helpful when combined with the ``__wired_factory__`` protocol and the ``@service_factory`` decorator discussed below.

Service factories accept one argument, a :class:`wired.ServiceContainer` instance.
The container may be used to get any dependencies required to create the service and return it from the factory.
The service is then cached on the container, available for any other factories or code to get.

The ``@service_factory`` decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's quite convenient to register your factories with decorators, as you can just point at a module or package and not manually do each registration.
``wired`` has optional support for the `venusian <https://pypi.org/project/venusian/>`_ package for deferred scanning and evaluation of decorators.
You can then register your services with the :class:`wired.service_factory` decorator:

.. literalinclude:: ../examples/decorators/basic_class.py
    :start-at: import service_factory
    :end-at: Hello from

The decorator can take arguments of ``for_``, ``context``, and ``name``, to mimic the arguments to ``register_factory``.

You can find more variations, including setup of the scanner, on this in the :ref:`examples-decorators` examples.

The ``__wired_factory__`` protocol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you call :meth:`wired.ServiceRegistry.register_factory` the first argument is the factory "function".
It takes a :class:`wired.ServiceContainer`, makes the desired object, and returns it.
This means a separation: a "function" that makes the class instance, and the class.

As we saw above, the first argument is really a callable that returns an instance, and that means the class itself can be the first argument.
But what if you want custom logic to pick apart the container then construct the class?

Enter the ``__wired_factory__`` protocol.
This is an attribute -- for example, a ``classmethod`` -- on the factory callable.
It is passed the container and returns the class.

.. literalinclude:: ../examples/wired_factory/register_wired_factory.py
    :start-at: @classmethod
    :end-at: return cls

This class method is then used as the first argument to :meth:`wired.ServiceRegistry.register_factory`.
It doesn't have to be just for classes and class methods: a function/class/instance could have a ``__wired_factory__`` attribute stamped on it, possibly via an intermediate decorator.

More examples are available in :ref:`examples-wired-factory`.

Example
~~~~~~~

.. code-block:: python

      from wired import ServiceRegistry

      def create_service_registry(settings):
          registry = ServiceRegistry()

          engine = engine_from_config(settings)
          registry.register_singleton(engine, name='dbengine')

          def dbsession_factory(container):
              engine = container.get(name='dbengine')
              return Session(bind=engine)
          registry.register_factory(dbsession_factory, name='dbsession')

          def login_factory(container):
              dbsession = container.get(name='dbsession')
              return LoginService(dbsession)
          registry.register_factory(login_factory, LoginService)

          return registry

      settings = ...
      registry = create_service_registry(settings)

Context-sensitive services
~~~~~~~~~~~~~~~~~~~~~~~~~~

A unique feature of ``wired`` is that different service factories/singletons can be registered for the same type/name.
The appropriate one is selected by registering the service with a ``context`` argument that constrains the types of context required.
At lookup-time a container is bound to a particular context and will affect which service factory is invoked.

Services are cached per-context instance (by object identity) and their factories can use the instance, defined as ``container.context`` as necessary.

By default, services are registered with ``context=None``, indicating that the service does not care and will not use the context.
In this case, the same instance will be cached and returned for any context.

Using services
--------------

The application / codebase, ideally, should define a single registry which is considered read-only and threadsafe.
Later, per-logical operation (such as a web request, or worker job, or thread, etc) a new :class:`wired.ServiceContainer` should be created.
The container can be used to create services required to complete the operation without concern for the exactly service implementation defined in the registry.

Example
~~~~~~~

.. code-block:: python

      container = registry.create_container()

      login_svc = container.get(LoginService)
      user = container.get(IUser, context=request.context)
      auth_token = login_svc.get_auth_token(user)

Binding to a context
~~~~~~~~~~~~~~~~~~~~

Container objects are thin wrappers around a service cache and it's possible to create more than one at a time, each bound to a different context in order to simplify calls to :meth:`wired.ServiceContainer.get`.
Bound containers are created automatically when invoking service factories if a ``context`` is passed to ``container.get(..., context=...)``. Alternatively, bind a container manually for reuse via :meth:`wired.ServiceContainer.bind`.
Using a bound container, all calls to ``.get`` will, by default, use the bound context.

Any factories registered for ``context=None`` (which is the default registration) will not be affected by any of this and will always receive a ``container.context`` value of ``None``.

Injecting services into a container manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes a service factory cannot easily be defined globally.
Rather, per-container there may be some services that can be registered, defined by the logical operation.

For example, imagine binding the web request itself as a service, or the active user:

.. code-block:: python

    container = registry.create_container()

    container.register_singleton(request, IRequest)
    container.register_singleton(request.user, IUser)

    # later ...

    user = container.get(IUser)

