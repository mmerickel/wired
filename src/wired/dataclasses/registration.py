from wired import ServiceRegistry
from .injector import Injector


def register_dataclass(
    registry: ServiceRegistry, target, for_=None, context=None, name=''
):
    """
    Register a factory for a dataclass that can sniff dependencies.

    .. code-block:: python

        from sqlalchemy.orm import Session

        @dataclass
        class LoginService:
            db: Session

        registry = ServiceRegistry()
        register_dataclass(registry, LoginService)

        # ... later
        container = registry.create_container()
        svc = container.get(LoginService)

    :param for_:
        By default, ``target`` is used as the service type. This can be used
        to override the ``iface_or_type`` argument in
        :meth:`wired.ServiceRegistry.register_factory` to some other type.

    :param context:
        The ``context`` argument in
        :meth:`wired.ServiceRegistry.register_factory`.

    :param str name:
        The ``name`` argument in
        :meth:`wired.ServiceRegistry.register_factory`.

    .. seealso::

        - :func:`wired.dataclasses.factory`

        - :func:`wired.dataclasses.injected`

    """
    # The common case, for default registrations we can omit
    # the "for_" as it is the same as the class implementing it
    if for_ is None:
        for_ = target

    injector = Injector(target)
    registry.register_factory(injector, for_, context=context, name=name)
