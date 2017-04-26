from unittest2 import TestCase

from pybot.listener import Listener

from .utils import Container, DummyMatcher


class ListenerTests(TestCase):
    def test_not_called_when_no_match(self):
        container = Container()
        func = self._new_response_func(container)
        listener = Listener(None, DummyMatcher(False), func)

        called = listener(None)

        self.assertFalse(called)
        self.assertIsNone(container.value)

    def test_called_when_match(self):
        container = Container()
        func = self._new_response_func(container)
        listener = Listener(None, DummyMatcher(True), func)

        called = listener(None)

        self.assertTrue(called)
        self.assertTrue(container.value)

    @staticmethod
    def _new_response_func(container):
        def response(res):
            container.value = res.match

        return response
