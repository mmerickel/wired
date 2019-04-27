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
