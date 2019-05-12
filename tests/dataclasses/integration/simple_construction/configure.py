# configure.py
from models import Greeter
from wired import ServiceRegistry
from wired.dataclasses import register_dataclass


def register(registry: ServiceRegistry):
    container = registry.create_container()
    register_dataclass(registry, Greeter)
