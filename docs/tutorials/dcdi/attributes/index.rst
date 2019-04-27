============================================
Limiting Surface Area to Injected Attributes
============================================

That looks quite nice.
One part that's not so nice: the ``Greeter`` has to ask for the entire ``Settings`` to be injected, then make a property to get the one part (``punctuation``) that it needs.

Let's introduce a Big Idea: a custom dataclass field that help manage the injection.
This ``injected`` field will act just like the ``field`` from dataclass.
But it will pack some things into the ``metadata`` structure on a dataclass ``field``.

In this case, we'll provide some instructions to the injector.
Namely, to get one attribute off the fetched item -- the ``punctuation`` -- and store it on the constructed dataclass.

With this in place, we can great decrease the surface area of the view.
Instead of asking for the entire Resource, just get the title.
Instead of the entire Greeter, just the greeting.

Along the way we do some other refactoring:

- The dataclass-autopilot thing is great, let's eliminate the rest of our ``factory`` staticmethods, except for one custom factory staticmethod, to show doing something funky

- But this brings up some special cases

- First, the ``Request`` wants the container. Change the injector to special-case look for a dataclass field that asks for it, and manually put ``container`` args rather than look it up

- Next, we'd prefer to look up the current URL with a class ``Url`` but then store a plain string value...let's use the new ``attr`` support to extract and store a ``str`` instead of a ``Url``

- Frozen dataclasses with slots

Code
====

``__init__.py``
---------------

.. literalinclude:: __init__.py

``models.py``
-------------

.. literalinclude:: models.py

``custom.py``
-------------

.. literalinclude:: custom.py

``utils.py``
------------

.. literalinclude:: utils.py