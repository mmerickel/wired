================
Custom Factories
================

It's nice using a generic factory that you don't have to write.
But sometimes you need more control and thus need a custom factory.

For example, you want to get a ``Customer`` from a little datastore, based on the current ``url``.
You can leave a ``classmethod`` named ``wired_factory`` on your dataclass to override the factory that ``wired.dataclasses`` generates for you.

As an example, let's make the "context" of a request into a first-class concept.
We expand our ``models.py`` with two more dataclasses:

.. literalinclude:: ../../tests/dataclasses/integration/custom_factory/models.py

- ``Request`` models the information coming in for this operation, namely the URL

- ``Context`` generates the current "context", meaning the resource being operated on. Our database only has ``Customer`` instances but it could later have more.

- ``Context`` has some special work for its factory, so it declares a ``wired_factory``

- ``Greeter`` no longer needs the customer name passed in...it can just ask for the ``Context``

Our app needs to do just a little bit more work to process the requests. Namely, it needs to make a ``Request`` and put it into the container, to kick things off:

.. literalinclude:: ../../tests/dataclasses/integration/custom_factory/request.py

Once the URL is available to the DI system, everything else can be injected. We finish off by assembling the app and processing a customer:

.. literalinclude:: ../../tests/dataclasses/integration/custom_factory/test_integration_custom_factory.py
    :start-after: start-after
