==================
Requests and Views
==================

As housekeeping, we remove the override part from the previous step.

Web frameworks, and even systems like ``pytest``, model individual units of work as a "request".
The request contains the information about the thing being worked on (the URL, the headers) along with other information unique to the operation. When finished, the request is thrown away.

Let's borrow that idea and that jargon. Each Customer coming through the door is part of a ``Request``.

Let's also steal another idea from web frameworks and use a ``View`` to collect all the information needed for generating a result, plus the logic to generate that result.

- "interaction" -> Request

- View manages the generation of the output

- Datastore is now a dict-like thing to get individual Customers

- The ``Url`` is stored in the container, so anything that wants to get the currently-processed URL, can ask the container for it

- Request is created from a request factory with the URL of the Customer and also stores the container (in case a View wants to do a lookup)

- A View factory which gets the Request, Context, and Greeter from the container, then renders the greeting

Code
====

``__init__.py``
---------------

.. literalinclude:: __init__.py

``custom.py``
-------------

.. literalinclude:: custom.py


``models.py``
-------------

.. literalinclude:: models.py
