=====
wired
=====

``wired`` is an implementation of an inversion of control (IoC) container and may be used as the core of a dependency injection (DI) framework or simply as a way to separate config-time from runtime for services in an application. It also provides caching such that a container maintains a local copy of each service as they are instantiated.

Installation
============

Stable release
--------------

To install ``wired``, run this command in your terminal:

.. code-block:: console

    $ pip install wired

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for ``wired`` can be downloaded from the `Github repo`_.

.. code-block:: console

    $ git clone https://github.com/mmerickel/wired.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install -e .

.. _Github repo: https://github.com/mmerickel/wired

Usage
=====

The basic workflow is:

1. Create a :class:`wired.ServiceRegistry` containing service factories and service singletons.

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

Service singletons and factories can be registered by type or by name. It is recommended to register them by type to avoid naming clashes. Two services registered for ``name='login'`` would clash and it would be unclear what each one is. However, a service factory that is registered to provide instances of the ``LoginService`` class are unambiguous. Anyone else registering such a service factory is directly competing for control of that type. It is possible to register for both type and name.

Service factories accept one argument, a :class:`wired.ServiceContainer` instance. The container may be used to get any dependencies required to create the service and return it from the factory. The service is then cached on the container, available for any other factories or code to get.

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

A unique feature of ``wired`` is that different service factories/singletons can be registered for the same type/name. The appropriate one is selected by registering the service with a ``context`` argument that constrains the types of context required. At lookup-time a container is bound to a particular context and will affect which service factory is invoked.

Services are cached per-context instance (by object identity) and their factories can use the instance, defined as ``container.context`` as necessary.

By default, services are registered with ``context=None``, indicating that the service does not care and will not use the context. In this case, the same instance will be cached and returned for any context.

Using services
--------------

The application / codebase, ideally, should define a single registry which is considered read-only and threadsafe. Later, per-logical operation (such as a web request, or worker job, or thread, etc) a new :class:`wired.ServiceContainer` should be created. The container can be used to create services required to complete the operation without concern for the exactly service implementation defined in the registry.

Example
~~~~~~~

.. code-block:: python

      container = registry.create_container()

      login_svc = container.get(LoginService)
      user = container.get(IUser, context=request.context)
      auth_token = login_svc.get_auth_token(user)

Binding to a context
~~~~~~~~~~~~~~~~~~~~

Container objects are thin wrappers around a service cache and it's possible to create more than one at a time, each bound to a different context in order to simplify calls to :meth:`wired.ServiceContainer.get`. Bound containers are created automatically when invoking service factories if a ``context`` is passed to ``container.get(..., context=...)``. Alternatively, bind a container manually for reuse via :meth:`wired.ServiceContainer.bind`. Using a bound container, all calls to ``.get`` will, by default, use the bound context.

Any factories registered for ``context=None`` (which is the default registration) will not be affected by any of this and will always receive a ``container.context`` value of ``None``.

Injecting services into a container manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes a service factory cannot easily be defined globally. Rather, per-container there may be some services that can be registered, defined by the logical operation.

For example, imagine binding the web request itself as a service, or the active user:

.. code-block:: python

    container = registry.create_container()

    container.set(request, IRequest)
    container.set(request.user, IUser)

    # later ...

    user = container.get(IUser)

More Information
================

.. toctree::
   :maxdepth: 1

   api
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
