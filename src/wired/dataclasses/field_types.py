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


class InjectedArgumentException(Exception):
    def __init__(self):
        msg = 'Cannot supply both attr and key arguments to inject'
        super().__init__(msg)


def injected(type_, **kwargs) -> Field:
    """ Get a value from an injected type

    We frequently want part of an injectable or adapter. Just an attribute
    or, for injectable/adapters that are dict-like, a key.

    This field type accepts an injectable/adapter and serves three purposes:

    - Get an attribute off of it by passing in attr='somevalue'

    - Or, get a key out of it by passing in key=''

    - Or, if the injectable/adapter has a __call__, return the value
      of calling it

    - Otherwise, return the injectable/adapter, same as if you didn't
      provide a field

     We could just manually do ``injected`` then pick apart the injected
     value. But that exposes a big surface area. This field type lets us
     zero in on what we want.
     """

    # First a sanity check, can't have both attr and key
    if 'attr' in kwargs and 'key' in kwargs:
        raise InjectedArgumentException()

    # If metadata was also passed in, preserve it, otherwise start clean
    if 'metadata' not in kwargs:
        kwargs['metadata'] = {}

    # Let's go in precedence
    kwm = kwargs['metadata']
    if 'attr' in kwargs:
        kwm['injected'] = dict(type_=type_, attr=kwargs['attr'])
        del kwargs['attr']
    elif 'key' in kwargs:
        kwm['injected'] = dict(type_=type_, key=kwargs['key'])
        del kwargs['key']
    elif 'call' in kwargs:
        # We'll presume that it is call=True
        kwm['injected'] = dict(type_=type_, call=kwargs['call'])
        del kwargs['call']
    else:
        # Default is to treat call=True if nothing else provided
        kwm['injected'] = dict(type_=type_, call=True)

    return field(**kwargs)
