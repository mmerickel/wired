"""

Dataclass field helpers.

It sucks to type:

.. code-block:: python

    sm_config: ServiceManagerConfig = field(
        metadata=dict(
            injected=True
        )
    )

These are some subclasses of field which wire up the common
cases.

"""
from dataclasses import field, Field
from zope.interface import Interface


def injected(
    iface_or_type=Interface, *, name='', attr=None, **kwargs
) -> Field:
    """
    Customize how the field is populated from the generated factory.

    If just the field type is insufficient, this descriptor can be used to
    more explicitly define how the field in the dataclass should be populated
    from the :class:`wired.ServiceContainer`.

    :param iface_or_type:
        The ``iface_or_type`` argument in :meth:`wired.ServiceContainer.get`.

    :param str name:
        The ``name`` argument in :meth:`wired.ServiceContainer.get`.

    :param str attr:
        An attribute on the returned service object.

    All other kwargs are forwarded directly into :func:`dataclasses.field`.

    """
    # If metadata was also passed in, preserve it, otherwise start clean
    if 'metadata' not in kwargs:
        kwargs['metadata'] = {}

    # Let's go in precedence
    kwm = kwargs['metadata']
    injected = kwm['injected'] = dict(type_=iface_or_type, name=name)
    if attr is not None:
        injected['attr'] = attr

    return field(**kwargs)
