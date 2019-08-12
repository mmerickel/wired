# app.py
from dataclasses import dataclass, field

from wired import ServiceRegistry


@dataclass
class App:
    registry: ServiceRegistry = field(default_factory=ServiceRegistry)
