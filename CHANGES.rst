0.4 (2024-02-22)
================

- Drop Python 3.5, 3.6, and 3.7.

- Add Python 3.9, 3.10, 3.11, and 3.12.

- Add a helpful error message if the ``name=`` argument is forgotten by
  simply passing a string directly into ``get('oops')``.
  See https://github.com/mmerickel/wired/pull/44

0.3 (2020-11-29)
================

- Added the ``__wired_factory__`` protocol which enables classes/functions.
  This feature allows objects to declare their factory in a reusable way
  near the definition of the class/function instead of near the
  ``ServiceRegistry.register_factory`` invocation. Build some decorators
  that automatically inject this protocol!
  See https://github.com/mmerickel/wired/pull/41

- Added the ``wired.service_factory`` venusian decorator which can be used
  to discover factories by setting up a ``venusian.Scanner`` and scanning
  your code to auto-register the services. In the future ``wired`` will likely
  provide top-level scanning, but for now you have to do it yourself and
  there are examples in the docs.
  See https://github.com/mmerickel/wired/pull/41

0.2.2 (2020-05-26)
==================

- Added a ``name`` argument to ``wired.dataclasses.register_dataclass``
  to support registering services by name.
  See https://github.com/mmerickel/wired/pull/32

- Removed the "how to write an injector" tutorial, then flatten a lot of the
  docs into no more than two levels (to please the RTD theme.)
  See https://github.com/mmerickel/wired/pull/32

0.2.1 (2019-08-12)
==================

- Added ``wired.dataclasses`` optional package with support for automatically
  generating service factories for Python 3.7's typed-dataclasses.
  Thanks Paul!
  See https://github.com/mmerickel/wired/pull/19

- Added a new tutorial on writing a DI framework around Python 3.7's
  typed-dataclasses. Thanks again Paul!
  See https://github.com/mmerickel/wired/pull/16

0.2 (2019-04-22)
================

Backward Incompatibilities
--------------------------

- ``wired.ServiceContainer.set`` has been redefined to set a service instance
  for a specific context object instead of for a type-of-context. The new
  method ``wired.ServiceContainer.register_singleton`` is a direct replacement
  for the old behavior.

Features
--------

- Add ``wired.ServiceContainer.register_factory`` and
  ``wired.ServiceContainer.register_singleton`` which are per-container
  analogues to their per-registry variants on ``wired.ServiceRegistry``.

- Edit docs to (a) improve sales pitch, (b) split into a couple of sub-pages,
  and (c) provide a tutorial. Update README and ``setup.py`` description a
  bit as well.
  See https://github.com/mmerickel/wired/pull/6

0.1.2 (2019-03-23)
==================

- Add support for Python 3.7.

- Fix an issue where two different service classes with the same name would
  be treated as the same service, defeating the type-based lookup.

0.1.1 (2018-08-04)
==================

- Improve memory management slightly in cases where many short-lived context
  objects are used by tracking and cleaning up their weakrefs.

0.1 (2018-08-01)
================

- Initial release.
