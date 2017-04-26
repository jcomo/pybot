from setuptools import setup, find_packages

setup(
    name = 'hubot-python',
    version = '0.0.1',
    description = "A python port of the popular Hubot",
    url = 'https://github.com/jcomo/pybot',
    author = 'Jonathan Como',
    author_email = 'jonathan.como@gmail.com',
    packages = find_packages(exclude=['docs', 'tests', 'scripts']),
    install_requires = ['six'],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'python chat bot framework automation script'
)
