from pybot.matchers import Matcher


class Container(object):
    def __init__(self):
        self.value = None


class DummyMatcher(Matcher):
    def __init__(self, match=True):
        self._match = match

    def match(self, message):
        return self._match


class FakeRobot(object):
    def __init__(self, name):
        self.name = name
