from dataclasses import dataclass
from .models import Settings


@dataclass
class Greeter:
    settings: Settings
