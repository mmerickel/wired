
Custom Factories
================

It's nice using a generic factory that you don't have to write.
Sometimes you need more control and thus need a custom factory.
For example, you want to get a ``Customer`` from a ``Datastore`` based on the current ``url``.

Just leave a ``classmethod`` named ``wired_factory`` on your dataclass

