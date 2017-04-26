import re


class Matcher(object):
    def match(self, message):
        pass


class RegexMatcher(Matcher):
    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    def match(self, message):
        if message.text:
            return self.regex.search(message.text)


class DirectMessageMatcher(Matcher):
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
