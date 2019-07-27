# models.py
from dataclasses import dataclass

from wired.dataclasses import factory


@factory()
@dataclass
class Settings:
    """ Store some configuration settings for the app """

    punctuation: str = '.'


@factory()
@dataclass
class Greeter:
    settings: Settings  # Ask DI to get the configured Settings
    name: str = 'Mary'

    def __call__(self, customer):
        punctuation = self.settings.punctuation
        return f'Hello {customer} my name is {self.name}{punctuation}'
