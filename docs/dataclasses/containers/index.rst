Containers
==========

Dataclass DI is usually done in the course of processing a unit of work, which usually means in a container.
Maybe you want to grab the container, then use ``__post_init__`` to pluck something out of the container:

.. xxxcode-block:: python

    from dataclasses import dataclass
    from typing import Optional

    from wired.dataclasses import factory

    from .models import Url


    @factory()
    @dataclass
    class Greeter:
        container: ServiceContainer
        url: Optional[str] = None

        def __post_init__(self):
            self.url = self.container.get(Url)

Yeh, that's kind of yucky.
We'll show an "attr" pattern later for this.
