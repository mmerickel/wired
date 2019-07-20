==========
Singletons
==========

We :doc:`just used <../simple_injection/index>` ``wired.dataclasses`` to register a ``wired`` factory -- in that case, ``Settings`` -- that was then used later.
Let's do the exact same thing, but with a ``wired`` *singleton*.

Let's change our ``Settings`` to a singleton but changing the ``factory`` decorator to ``singleton``:

Everything is the same as in :doc:`../decorators/index`, we just have different models:

.. literalinclude:: models.py
    :emphasize-lines: 4, 7

And...that's it, no other changes.