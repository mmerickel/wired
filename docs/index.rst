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

Example
=======

Imagine an application where customers walk in the door and you want a `Greeter` to greet them:

.. code-block:: python

    class Greeter:
        def __init__(self, greeting):
            self.greeting = greeting

        def __call__(self):
            return self.greeting + ' !!'

Our application is pluggable: it has a "registry" which processes operations in a "container":

>>> from wired import ServiceRegistry
>>> registry = ServiceRegistry()

As part of application setup, stuff gets put in the app's registry.  This application is simple: there's only one Greeter, so we register a "singleton" `Greeter` instance:

.. code-block:: python

    # Greeters are nice...they greet people!
    greeter = Greeter(greeting='Hello')

    # Register it as a singleton using its class for the "key"
    registry.register_singleton(greeter, Greeter)

Here is a function that greets a customer as part of a "container" operation:

.. code-block:: python

    def greet_a_customer(container):

        # Ask the *system* via the container to find the `Greeter` for us
        the_greeter = container.get(Greeter)
        greeting = the_greeter()

        return greeting

The app processes a customer by making a container and doing the operation:

>>> container = registry.create_container()
>>> greeting = greet_a_customer(container)
>>> print(greeting)
Hello !!

For a deeper introduction, try :doc:`the Tour of Wired tutorial <./tutorials/tour/index>`.

More Information
================

.. toctree::
   :maxdepth: 1

   usage
   tutorials/index
   dc/index
   api
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
