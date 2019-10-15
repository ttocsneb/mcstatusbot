import os
from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


# All the pip dependencies required for installation.
INSTALL_REQUIRES = [
    'discord.py>=1.2.2',
    'ruamel.yaml',
    'marshmallow',
    'mcstatus',
    # 'SQLAlchemy',
    # 'alembic'
]


def params():

    name = "Discord Minecraft Server Status Bot"

    version = "0.1"

    description = "A discord bot that displays the status of a minecraft server"

    long_description = LONG_DESCRIPTION
    long_description_content_type = "text/markdown"

    install_requires = INSTALL_REQUIRES

    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications :: Chat"
    ]
    author = 'Benjamin Jacobs'
    url = 'https://github.com/ttocsneb/mcstatusbot'

    packages = ['mcstatusbot']

    entry_points = {
        'console_scripts': [
            'mcstatusbot = mcstatusbot:serve'
        ]
    }

    return locals()


setup(**params())
