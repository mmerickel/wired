Attributes
==========

Asking for ``Settings`` has two downsides:

- It's a pretty big surface area, maybe we only wanted a single value

- The single value we want probably isn't of type ``Settings``, it's probably a string.

``wired.dataclases`` provides a custom ``dataclass`` field called ``injected``:

.. xxxcode-block:: python

    from wired.dataclasses import injected

    @factory()
    @dataclass
    class Greeter:
        greeting: str = injected(Settings, attr='greeting')

Behind the scenes this is the same as:

.. xxxcode-block:: python

    from dataclasses import field

    @factory()
    @dataclass
    class Greeter:
        greeting: str = field(metadata=dict(injected=dict(type_=Settings, attr='greeting')))

Easier on the eyes.

The ``injected`` field uses the ``metadata`` support in dataclass fields to make a custom protocol, giving special instructions to the DI system on how to construct the dataclass.

For example, these two are equivalent:

.. xxxcode-block:: python

    @factory()
    @dataclass
    class Greeter1:
        settings: Settings = injected(Settings)

    @factory()
    @dataclass
    class Greeter2:
        settings: Settings

With ``attr`` our DI contract with "the system" is more targeted.
Instead of asking for all of ``Settings``, we just get what we need.
Perhaps we want two things out of ``Settings``:

.. xxxcode-block:: python

    @factory()
    @dataclass
    class Greeter:
        greeting: str = injected(Settings, attr='greeting')
        punctuation: str = injected(Settings, attr='punctuation')
