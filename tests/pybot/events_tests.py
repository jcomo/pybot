from unittest2 import TestCase

from pybot.events import EventBus

from .utils import Container


class EventBusTests(TestCase):
    def setUp(self):
        self.bus = EventBus()

    def test_publish_no_subscribers(self):
        self.bus.publish('test')

    def test_publish_multiple_subscribers(self):
        container1 = Container()
        subscriber1 = self._new_subscriber(container1)

        container2 = Container()
        subscriber2 = self._new_subscriber(container2)

        self.bus.subscribe('test', subscriber1)
        self.bus.subscribe('test', subscriber2)

        self.bus.publish('test', {'value': 2})

        self.assertEquals(2, container1.value)
        self.assertEquals(2, container2.value)

    def test_publish_multiple_types(self):
        container1 = Container()
        subscriber1 = self._new_subscriber(container1)

        container2 = Container()
        subscriber2 = self._new_subscriber(container2)

        self.bus.subscribe('test1', subscriber1)
        self.bus.subscribe('test2', subscriber2)

        self.bus.publish('test1', {'value': 2})

        self.assertEquals(2, container1.value)
        self.assertIsNone(container2.value)

    def test_unsubscribe(self):
        container1 = Container()
        subscriber1 = self._new_subscriber(container1)

        container2 = Container()
        subscriber2 = self._new_subscriber(container2)

        self.bus.subscribe('test', subscriber1)
        self.bus.subscribe('test', subscriber2)
        self.bus.unsubscribe('test', subscriber1)

        self.bus.publish('test', {'value': 2})

        self.assertIsNone(container1.value)
        self.assertEquals(2, container2.value)

    @staticmethod
    def _new_subscriber(container):
        def subscriber(data):
            container.value = data.get('value')

        return subscriber
