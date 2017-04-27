from unittest2 import TestCase

from pybot.matchers import Matcher, RegexMatcher, RobotNameMatcher
from pybot.messages import Message

from .utils import DummyMatcher, FakeRobot


class RegexMatcherTests(TestCase):
    def setUp(self):
        self.matcher = RegexMatcher(r"the (.*?) fox")

    def test_message_with_no_text(self):
        message = Message(None, None, None)
        self.assertIsNone(self.matcher.match(message))

    def test_regex_does_not_match(self):
        message = Message(None, None, "the fox")
        self.assertIsNone(self.matcher.match(message))

    def test_regex_matches(self):
        message = Message(None, None, "the quick fox")
        match = self.matcher.match(message)
        self.assertEquals("quick", match.group(1))


class RobotNameMatcherTests(TestCase):
    def setUp(self):
        self.robot = FakeRobot('Fred')
        self.matcher = RobotNameMatcher(DummyMatcher(), self.robot)

    def test_message_with_no_text(self):
        message = Message(None, None, None)
        self.assertIsNone(self.matcher.match(message))

    def test_empty_message_text(self):
        message = Message(None, None, "")
        self.assertIsNone(self.matcher.match(message))

    def test_does_not_match_name(self):
        message = Message(None, None, "hubot say hello")
        self.assertIsNone(self.matcher.match(message))

    def test_matches_name(self):
        message = Message(None, None, "fred say hello")
        self.assertTrue(self.matcher.match(message))

    def test_matches_name_with_extra_chars(self):
        message = Message(None, None, "@fred: say hello")
        self.assertTrue(self.matcher.match(message))

    def test_matches_name_after_being_changed(self):
        self.robot.name = 'Ted'
        message = Message(None, None, "ted say hello")
        self.assertTrue(self.matcher.match(message))
