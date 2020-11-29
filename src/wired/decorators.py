# wired is usable without venusian
try:
    import venusian
except ImportError:  # pragma: no cover
    venusian = None


# noinspection PyPep8Naming
class service_factory:
    """
    Register a factory for a class that can sniff dependencies.

    The factory will be registered with a :class:`wired.ServiceRegistry` when
    performing a venusian scan.

    .. seealso::

        - :func:`wired.ServiceRegistry.register_factory`

    """

    def __init__(self, for_=None, context=None, name: str = ''):
        self.for_ = for_
        self.context = context
        self.name = name

    def __call__(self, wrapped):
        def callback(scanner: venusian.Scanner, name: str, cls):
            registry = getattr(scanner, 'registry')
            # If there is a for_ use it, otherwise, register for the same
            # class as the instance
            for_ = self.for_ if self.for_ else cls

            registry.register_factory(
                cls, for_, context=self.context, name=self.name
            )

        venusian.attach(wrapped, callback, category='wired')
        return wrapped
