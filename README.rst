=====
wired
=====

.. image:: https://img.shields.io/pypi/v/wired.svg
    :target: https://pypi.org/pypi/wired

.. image:: https://img.shields.io/travis/mmerickel/wired/master.svg
    :target: https://travis-ci.org/mmerickel/wired

.. image:: https://readthedocs.org/projects/wired/badge/?version=latest
    :target: https://readthedocs.org/projects/wired/?badge=latest
    :alt: Documentation Status

Have a large application where you want to *decrease coupling* between components?
Need to *supply configuration* to your application's various services? Want to
make a *pluggable application* where others can supply services?

`Inversion of Control <https://en.wikipedia.org/wiki/Inversion_of_control>`_ and
`Dependency Injection <https://en.wikipedia.org/wiki/Dependency_injection>`_ are
two patterns commonly used for these goals.

``wired`` is an implementation of an inversion-of-control (IoC) container and
may be used as the core of a dependency injection (DI) framework or simply as
a way to separate config-time from runtime for services in an application. It
also provides caching such that a container maintains a local copy of each
service as they are instantiated.

`wired` aims to scale down to the simplest cases and up to very large, custom
systems. It has one dependency and that dependency has one dependency.

See https://wired.readthedocs.io or
``docs/index.rst`` in this distribution for detailed documentation.
