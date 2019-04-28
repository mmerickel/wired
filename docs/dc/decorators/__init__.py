from .app import App
from .models import Greeter


def main():
    site = App()
    with site as container:
        greeter = container.get(Greeter)
        greeting = greeter('Larry')
        return 'Hello Larry my name is Mary' == greeting
