# from dataclasses import dataclass, field
# from typing import Sequence
#
# from venusian import Scanner
#
# from wired import ServiceRegistry
#
#
# @dataclass
# class DI:
#     """ Bundle all the pieces into a dependency injection system. """
#
#     registry: ServiceRegistry = field(default_factory=ServiceRegistry)
#     scanner: Scanner = field(init=False)
#
#     def __post_init__(self):
#         self.scanner = Scanner(
#             registry=self.registry,
#             di=self
#         )
#
#     def scan(self, targets: Sequence):
#         """ Use Venusian to process the target modules """
#
#         [
#             self.scanner.scan(target)
#             for target in targets
#         ]
