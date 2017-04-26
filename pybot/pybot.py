import re
from collections import namedtuple
from os import environ as env

from six import print_
from six.moves import input

User = namedtuple('User', ['id', 'name', 'room'])


class Message(object):
    def __init__(self, user):
        self.user = user
        self.room = user.room
        self.text = None
        self.id = None


class TextMessage(Message):
    def __init__(self, user, text, id):
        super(TextMessage, self).__init__(user)
        self.text = text
        self.id = id


class Adapter(object):
    def __init__(self, robot):
        self.robot = robot

    def send(self, message, text):
        pass

    def emote(self, message, text):
        self.send(message, text)

    def reply(self, message, text):
        pass

    def topic(self, message, text):
        pass

    def play(self, message, text):
        pass

    def run(self):
        pass

    def close(self):
        pass

    def receive(self, text):
        self.robot.receive(text)


class ShellAdapter(Adapter):
    def send(self, message, text):
        print(text)

    def emote(self, message, text):
        self.send(message, '* {}'.format(text))

    def reply(self, message, text):
        self.send(message, '{}: {}'.format(message.user.name, text))

    def run(self):
        stopped = False
        name = env.get('PYBOT_SHELL_USER_NAME', 'Shell')

        try:
            user_id = env.get('PYBOT_SHELL_USER_ID')
        except ValueError:
            user_id = 1

        while True:
            try:
                text = input('{}> '.format(self.robot.name))
            except EOFError:
                print
                break

            if text == 'quit':
                break

            user = User(user_id, name, 'shell')
            message = TextMessage(user, text, 'message_id')
            self.receive(message)

        self.robot.shutdown()


class Response(object):
    def __init__(self, robot, message, match):
        self.robot = robot
        self.message = message
        self.match = match.group

    def send(self, text):
        self.robot.adapter.send(self.message, text)

    def emote(self, text):
        self.robot.adapter.emote(self.message, text)

    def reply(self, text):
        self.robot.adapter.reply(self.message, text)

    def topic(self, text):
        self.robot.adapter.topic(self.message, text)


class Robot(object):
    def __init__(self, name='Pybot'):
        self.name = name
        self._load_adapter()
        self._listeners = []

    def _load_adapter(self):
        # TODO: dynamically load the adapter based on args
        # TODO: catch all errors and exit if failure to load
        self.adapter = ShellAdapter(self)

    def run(self):
        self.adapter.run()

    def shutdown(self):
        # TODO
        pass

    def receive(self, message):
        for matcher, response_func in self._listeners:
            match = matcher.match(message)
            if not match:
                continue

            response = Response(self, message, match)
            response_func(response)

    def respond(self, pattern):
        def wrapper(f):
            matcher = TextMatcher(pattern)
            wrapper = NameMatcher(matcher, self.name)
            self._add_listener(wrapper, f)

        return wrapper

    def hear(self, pattern):
        # TODO: wraps?
        def wrapper(f):
            matcher = TextMatcher(pattern)
            self._add_listener(matcher, f)

        return wrapper

    def listen(self, matcher):
        def wrapper(f):
            self._add_listener(matcher, f)

        return wrapper

    def _add_listener(self, matcher, response_func):
        self._listeners.append((matcher, response_func))


class Matcher(object):
    def match(self, message):
        pass


class TextMatcher(Matcher):
    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    def match(self, message):
        if message.text:
            return self.regex.search(message.text)


class NameMatcher(Matcher):
    def __init__(self, wrapped, name):
        self.wrapped = wrapped
        self.name = name.lower()

    def match(self, message):
        if not message.text:
            return

        tokens = message.text.lower().split(' ')
        if not tokens:
            return

        first_token = tokens[0].lstrip(' ').rstrip(' :-=')
        if first_token == self.name:
            return self.wrapped.match(message)

