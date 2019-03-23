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
