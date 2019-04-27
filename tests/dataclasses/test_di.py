# from dataclasses import dataclass
#
# from venusian import Scanner
#
# from wired import ServiceRegistry, ServiceContainer
# from wired.dataclasses import DI, factory
#
#
# @factory()
# @dataclass
# class Greeter01:
#     name: str = 'greeter_one'
#
#
# def test_construction():
#     di = DI()
#     assert DI is di.__class__
#
#
# def test_no_registry_passed_in():
#     di = DI()
#     assert ServiceRegistry is di.registry.__class__
#
#
# def test_registry_passed_in():
#     registry = ServiceRegistry()
#     di = DI(registry=registry)
#     assert registry is di.registry
#
#
# def test_scanner():
#     di = DI()
#     assert Scanner is di.scanner.__class__
#
#
# def test_scan():
#     di = DI()
#     m = __import__(__name__)
#     targets = (m,)
#     di.scan(targets)
#     # Now try to get something from the registry
#     container = di.registry.create_container()
#     greeter = container.get(Greeter01)
#     assert Greeter01 is greeter.__class__
#
#     @dataclass
#     class Url:
#         name: str = 'url'
#
#     container.set(99, Url)
#     u = container.get(Url)
#     assert 989 == u
