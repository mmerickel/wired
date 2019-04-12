=====
wired
=====

*An inversion-of-control (IoC) container for building decoupled, extensible, configurable, pluggable applications.*

Have a large application where you want to *decrease coupling* between components?
Need to *supply configuration* to your application's various services?
Want to make a *pluggable application* where others can supply services?

`Inversion of Control <https://en.wikipedia.org/wiki/Inversion_of_control>`_ and `Dependency Injection <https://en.wikipedia.org/wiki/Dependency_injection>`_ are two patterns commonly used for these goals.

``wired`` is an implementation of an inversion-of-control (IoC) container and may be used as the core of a dependency injection (DI) framework or simply as a way to separate config-time from runtime for services in an application.
It also provides caching such that a container maintains a local copy of each service as they are instantiated.

`wired` aims to *scale down* to the simplest cases and *scale up* to very large, custom systems.
It has one dependency and that dependency has one dependency.

Installation
============

Stable release
--------------

To install ``wired``, run this command in your terminal:

.. code-block:: console

    $ pip install wired

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for ``wired`` can be downloaded from the `Github repo`_.

.. code-block:: console

    $ git clone https://github.com/mmerickel/wired.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install -e .

.. _Github repo: https://github.com/mmerickel/wired

Quick Usage
===========

Imagine an application where customers walk in the door and you want to greet them with a Greeter. This application is simple: there's only one Greeter.

To do this, we:

- Setup the application: make a "registry" and register some things (a "singleton" to hold the ``Greeter``)

- Start processing requests (greet someone) by getting stuff we need to process the request

- "Get stuff we need" by asking *the system* for what we need (a ``Greeter``)

For a deeper dive, try :doc:`the tutorial <./tutorial/index>`.

.. literalinclude:: examples/simple_example.py

More Information
================

.. toctree::
   :maxdepth: 1

   usage
   tutorial/index
   api
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
