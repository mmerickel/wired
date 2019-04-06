import weakref
from zope.interface import Interface, implementedBy, providedBy
from zope.interface.interface import InterfaceClass
from zope.interface.interfaces import IInterface
from zope.interface.adapter import AdapterRegistry


__all__ = ['ServiceContainer', 'ServiceRegistry']


class Sentinel:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<' + self.name + '>'


_marker = Sentinel('default')


class IServiceFactory(Interface):
    """ A marker interface for service factories."""


class IServiceInstance(Interface):
    """ A marker interface for service instances."""


class IContextFinalizer(Interface):
    """ A marker interface for a finalizer invocable when a context dies."""


class ServiceFactoryInfo:
    def __init__(self, factory, service_iface, context_iface, wants_context):
        self.factory = factory
        self.service_iface = service_iface
        self.context_iface = context_iface
        self.wants_context = wants_context


class SingletonServiceWrapper:
    def __init__(self, service):
        self.service = service

    def __call__(self, services):
        return self.service


class ServiceCache:
    """
    A per-context registry that avoids leaking memory when a context object
    is garbage collected.

    The goal of the cache is to keep any instantiated services alive for
    ``min(context_lifetime, self_lifetime)``.

    """

    _AdapterRegistry = AdapterRegistry  # for testing

    def __init__(self):
        self.contexts = {}
        self.ref = weakref.ref(self)

    def __del__(self):
        # try to remove the finalizers from the contexts incase the context
        # is still alive, there's no sense in having a weakref attached to it
        # now that the cache is dead
        for ctx_id, ctx_cache in self.contexts.items():
            finalizer = ctx_cache.lookup(
                (), IContextFinalizer, name='', default=_marker
            )
            if finalizer is not _marker:  # pragma: no cover
                finalizer.detach()

    def get(self, context):
        ctx_id = id(context)
        ctx_cache = self.contexts.get(ctx_id, None)
        if ctx_cache is None:
            ctx_cache = self._AdapterRegistry()
            try:
                finalizer = weakref.finalize(
                    context,
                    context_finalizer,
                    cache_ref=self.ref,
                    ctx_id=ctx_id,
                )
            except TypeError:
                # not every type supports weakrefs, in which case we
                # simply cannot release the ctx_cache early
                pass
            else:
                finalizer.atexit = False
                ctx_cache.register((), IContextFinalizer, '', finalizer)
            self.contexts[ctx_id] = ctx_cache
        return ctx_cache


def context_finalizer(cache_ref, ctx_id):  # pragma: no cover
    # if the context lives longer than self then remove it
    # to avoid keeping any refs to the registry
    cache = cache_ref()
    if cache is not None and ctx_id in cache.contexts:
        del cache.contexts[ctx_id]


class ServiceContainer:
    """
    A service container is used to create service instances.

    Create a container via :meth:`wired.ServiceRegistry.create_container`.

    A container controls creating services from the registered factories.
    Services are cached based on their registration constraints and re-used
    when possible based on the context and requested interface.

    """

    _ServiceCache = ServiceCache  # for testing

    def __init__(self, factories, cache=None, context=None):
        if cache is None:
            cache = self._ServiceCache()
        self.factories = factories
        self.cache = cache
        self.context = context

    def bind(self, *, context):
        """
        Return a new container sharing the same cache but bound to ``context``.

        """
        if context is self.context:
            return self
        return self.__class__(
            factories=self.factories, cache=self.cache, context=context
        )

    def set(
        self, service, iface_or_type=Interface, *, context=Interface, name=''
    ):
        """
        Add a service instance to the container.

        Upon success, ``service`` will be returned for any uncached lookups.

        If this service registration would affect a previously-cached lookup
        then it will raise a ``ValueError``.

        :param service: A service instance to cache.
        :param iface_or_type: A class or ``zope.interface.Interface`` object
            defining the interface of the service. Defaults to
            ``zope.interface.Interface`` to match any requested interface.
        :param context: A class or ``zope.interface.Interface`` object
            defining the type of :attr:`.context` required in order to use
            the factory. Defaults to ``zope.interface.Interface`` to match
            any context.
        :param str name: An identifier for the service.

        """
        iface = _iface_for_type(iface_or_type)
        context_iface = _iface_for_context(context)
        cache = self.cache.get(None)

        inst = cache.lookup(
            (IServiceInstance, context_iface),
            iface,
            name=name,
            default=_marker,
        )
        if inst is not _marker:
            raise ValueError(
                'a service instance is already cached that would conflict '
                'with this registration'
            )

        cache.register((IServiceInstance, context_iface), iface, name, service)

    def get(
        self,
        iface_or_type=Interface,
        *,
        context=_marker,
        name='',
        default=_marker
    ):
        """
        Find a cached instance or create one from the registered factory.

        The instance is found using the following algorithm:

            1. Find an instance matching the criteria in the container. If one
               is found, return it directly.

            2. If no instance is found, search for the factory on the registry.
               If one is not found, raise a ``LookupError``.

            3. Instiantiate the factory, caching the result in the container.

        :param iface_or_type: The registered service interface.
        :param context: A context object. This object will be available as
            ``container.context`` in the invoked service factories and will
            influence which factories are matched. Defaults to the bound
            :attr:`.context` on the container.
        :param str name: The registered name of the service.

        """
        if context is not _marker and context is not self.context:
            proxy = self.bind(context=context)
            return proxy.get(iface_or_type, name=name, default=default)

        context = self.context
        iface = _iface_for_type(iface_or_type)
        context_iface = providedBy(context)
        cache = self.cache.get(context)

        inst = cache.lookup(
            (IServiceInstance, context_iface),
            iface,
            name=name,
            default=_marker,
        )
        if inst is not _marker:
            return inst

        # there is no instance registered for this context, fallback to
        # see if there is one registered for context=None before falling
        # back to factories, this would normally be from a call to .set()
        if context is not None:
            inst = self.cache.get(None).lookup(
                (IServiceInstance, context_iface),
                iface,
                name=name,
                default=_marker,
            )
            if inst is not _marker:
                return inst

        svc_info = self.factories.lookup(
            (IServiceFactory, context_iface), iface, name=name, default=_marker
        )
        if svc_info is _marker:
            if default is not _marker:
                return default
            raise LookupError('could not find registered service factory')

        # there is no service registered for this context, fallback
        # to see if there is one registered for context=None by hiding
        # the current context for the remainder of the lookup
        if not svc_info.wants_context and context is not None:
            proxy = self.bind(context=None)
            return proxy.get(iface_or_type, name=name, default=default)

        inst = svc_info.factory(self)

        # make sure to register the service using the original, general
        # context_iface, not the provided one as it may be more specific
        cache.register(
            (IServiceInstance, svc_info.context_iface),
            svc_info.service_iface,
            name,
            inst,
        )
        return inst


class ServiceRegistry:
    """
    A service registry contains service factory definitions.

    Define the tree of services your application needs once at config-time.
    Later, per operation, invoke :meth:`.create_container` to create a new
    service container which can be used to lazily instantiate service
    objects on-demand.

    Using this pattern, your code now depends on the container and your
    service interfaces. You are now programming to an interface, not to a
    specific implementation. It is now trivial to register a different
    factory to mock out, or replace, specific service implementations in
    tests or for any other purposes.

    """

    _AdapterRegistry = AdapterRegistry  # for testing
    _ServiceContainer = ServiceContainer  # for testing

    def __init__(self, factory_registry=None):
        if factory_registry is None:
            factory_registry = self._AdapterRegistry()
        self.factories = factory_registry

    def create_container(self, *, context=None):
        """
        Create a new :class:`wired.ServiceContainer` linked to the registry.

        A container will use all the registered service factories,
        independently of any other containers, in order to find and
        instantiate service objects.

        Practically, a new container should be derived per logical
        "operation". An operation is something like a web request, job,
        transaction, etc.

        :param context: The container will be bound to a different context
            object, affecting which factories are selected. By default,
            the container is bound to the ``None`` context.

        """
        return self._ServiceContainer(self.factories, context=context)

    def register_factory(
        self, factory, iface_or_type=Interface, *, context=None, name=''
    ):
        """
        Register a service factory.

        A factory should accept a single parameter which will be a
        :class:`.ServiceContainer` instance. The factory should not be bound
        to any particular container and should use the one passed in to find
        service dependencies.

        A factory can be registered for a particular type or interface, with
        more specific factories allowed per type of ``context`` or by
        ``name`` string.

        It is recommended to register factories using types/interfaces instead
        of named strings, as they avoid naming clashes between independently
        defined components/features. Types are always unique and are better
        at expressing intent and contracts.

        An example service factory:

        .. code-block:: python

            def login_factory(container):
                dbsession = container.get(name='dbsession')
                return LoginService(dbsession)

        Notice in the above example that the ``login_factory`` requires
        another service named ``db`` to be registered which triggers a
        recursive lookup for that service in order to create the
        ``LoginService`` instance.

        It is not required that the returned service actually implements,
        or is a subclass, of the defined ``iface``.

        :param factory: A factory is a callable that accepts a container
            argument and returns an instance of the service. Specifically,
            ``factory(services: ServiceContainer) -> iface``.
        :param iface_or_type: A class or ``zope.interface.Interface`` object
            defining the interface of the service. Defaults to
            ``zope.interface.Interface`` to match any requested interface.
        :param context: A class or ``zope.interface.Interface`` object
            defining the type of :attr:`.context` required in order to use
            the factory. Defaults to ``None``.
        :param str name: An identifier for the service. A factory can be
            registered for an ``iface_or_type`` or a ``name`` or both, but an
            ``iface_or_type`` is recommended for most services.

        """
        iface = _iface_for_type(iface_or_type)
        context_iface = _iface_for_context(context)
        wants_context = context is not None

        info = ServiceFactoryInfo(factory, iface, context_iface, wants_context)
        self.factories.register(
            (IServiceFactory, context_iface), iface, name, info
        )

    def register_singleton(
        self, service, iface_or_type=Interface, *, context=None, name=''
    ):
        """
        Register a singleton instance.

        The singleton is global to all containers created from this registry.
        Any container created by this registry will receive the same instance.

        Functionally, the singleton is wrapped in a factory that always
        returns the same instance when invoked. See :meth:`.register_factory`
        for information on the parameters.

        """
        service_factory = SingletonServiceWrapper(service)
        return self.register_factory(
            service_factory, iface_or_type, context=context, name=name
        )

    def find_factory(self, iface_or_type=Interface, *, context=None, name=''):
        """
        Return the factory registered for the given parameters.

        The arguments are the same as those used in :meth:`.register_factory`.

        :returns: The registered factory (or singleton wrapper) or ``None``
            if a factory cannot be found satisfying the constraints.

        """
        iface = _iface_for_type(iface_or_type)
        context_iface = _iface_for_context(context)

        svc_info = self.factories.lookup(
            (IServiceFactory, context_iface), iface, name=name, default=_marker
        )
        if svc_info is not _marker:
            return svc_info.factory


def _iface_for_type(obj):
    # if the object is an interface then we can quit early
    if IInterface.providedBy(obj):
        return obj

    # look for a cached iface
    iface = obj.__dict__.get('_service_iface', None)
    if iface is not None:
        return iface

    # make a new iface and cache it on the object
    name = obj.__qualname__
    iface = InterfaceClass(
        '%s_%s_IService' % (name, id(obj)),
        __doc__='service_factory generated interface',
    )
    obj._service_iface = iface
    return iface


def _iface_for_context(obj):
    if obj is None:
        return Interface
    elif not IInterface.providedBy(obj):
        return implementedBy(obj)
    return obj
