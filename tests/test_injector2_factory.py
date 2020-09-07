# from typing import cast
#
# from wired import ServiceContainer
# from wired.injector2 import Injector
#
#
# class DummyContainer:
#     def __init__(self, context=None):
#         self.context = None
#
#
# class DummyService:
#     """ Some marker """
#     pass
#
#
# def test_function_no_args():
#     """ The callable has no arguments """
#
#     class ThisContainer(DummyContainer):
#         def get(self, service):
#             pass  # Unused in this test
#
#     def dummy_service():
#         return 99
#
#     container = cast(ServiceContainer, ThisContainer())
#     injector = Injector(container=container, target=dummy_service)
#     result = injector()
#     assert 9 == result[0][2]
